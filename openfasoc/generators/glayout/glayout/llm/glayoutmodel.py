import pandas as pd
import torch
from transformers import BertTokenizer, BertModel

# Load the pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Load the training data
train_data = pd.read_csv('train.csv')

# Preprocess the data
input_ids = []
attention_masks = []
labels = []

for text, label in train_data.values:
	inputs = tokenizer.encode_plus(
		text,
		add_special_tokens=True,
		max_length=512,
		padding='max_length',
		truncation=True,
		return_attention_mask=True,
		return_tensors='pt'
	)
	input_ids.append(inputs['input_ids'].flatten())
	attention_masks.append(inputs['attention_mask'].flatten())
	labels.append(label)

# Convert lists to tensors
input_ids = torch.tensor(input_ids)
attention_masks = torch.tensor(attention_masks)
labels = torch.tensor(labels)

# Define a custom dataset class
class GlayoutDataset(torch.utils.data.Dataset):
	def __init__(self, input_ids, attention_masks, labels):
		self.input_ids = input_ids
		self.attention_masks = attention_masks
		self.labels = labels

	def __len__(self):
		return len(self.input_ids)

	def __getitem__(self, idx):
		input_ids = self.input_ids[idx]
		attention_masks = self.attention_masks[idx]
		labels = self.labels[idx]
		return {
			'input_ids': input_ids,
			'attention_mask': attention_masks,
			'labels': labels
		}

# Create a dataset and data loader
dataset = GlayoutDataset(input_ids, attention_masks, labels)
data_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)


# Define a custom model class
class GlayoutModel(BertModel):
	def __init__(self, num_labels):
		super(GlayoutModel, self).__init__()
		self.num_labels = num_labels
		self.dropout = torch.nn.Dropout(0.1)
		self.fc = torch.nn.Linear(self.config.hidden_size, num_labels)

	def forward(self, input_ids, attention_mask):
		outputs = super(GlayoutModel, self).forward(
			input_ids=input_ids,
			attention_mask=attention_mask
		)
		pooler_output = outputs.pooler_output
		pooler_output = self.dropout(pooler_output)
		outputs = self.fc(pooler_output)
		return outputs

# Initialize the custom model
model = GlayoutModel(num_labels=len(glayoutactions))

# Fine-tune the model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

for epoch in range(5):
	model.train()
	total_loss = 0
	for batch in data_loader:
		input_ids = batch['input_ids'].to(device)
		attention_mask = batch['attention_mask'].to(device)
		labels = batch['labels'].to(device)
		optimizer.zero_grad()
		outputs = model(input_ids, attention_mask)
		loss = criterion(outputs, labels)
		loss.backward()
		optimizer.step()
		total_loss += loss.item()
	print(f'Epoch {epoch+1}, Loss: {total_loss / len(data_loader)}')

# Evaluate the model
model.eval()
eval_results = []
with torch.no_grad():
	for batch in data_loader:
		input_ids = batch['input_ids'].to(device)
		attention_mask = batch['attention_mask'].to(device)
		labels = batch['labels'].to(device)
		outputs = model(input_ids, attention_mask)
		logits = outputs.detach().cpu().numpy()
		label_ids = labels.detach().cpu().numpy()
		eval_results.extend(zip(logits, label_ids))

# Use the fine-tuned model to generate strict syntax output
def generate_syntax(text):
	input_ids = tokenizer.encode(text, return_tensors='pt')
	attention_mask = tokenizer.encode(text, return_tensors='pt', max_length=512, padding='max_length', truncation=True)
	outputs = model(input_ids, attention_mask)
	logits = outputs.detach().cpu().numpy()
	predicted_label = GlayoutActions(logits.argmax())
	return predicted_label

# Example usage:
text = "This is a sample input text"
syntax_output = generate_syntax(text)
print(syntax_output)
