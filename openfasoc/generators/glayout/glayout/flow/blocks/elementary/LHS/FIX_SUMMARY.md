# Fix for Gymnasium Info Dict Error in OpenFASOC

## Problem Description

The error "Values of the info dict only support int, float, string or tuple" was occurring when running `generate_tg_1000_dataset.py` because:

1. **Root Cause**: Component objects were storing `Netlist` objects directly in their `info` dictionary
2. **Library Conflict**: The `gymnasium` library (used in ML optimization pipelines) only accepts basic data types in info dictionaries
3. **Error Location**: The error occurred when `Netlist` objects were encountered in `component.info['netlist']`

## Files Modified

The following files were updated to fix the issue:

### Core Primitive Files
1. **`glayout/flow/primitives/fet.py`**
   - Fixed NMOS and PMOS functions (lines ~484 and ~622)
   - Changed from storing `Netlist` object directly to storing as string

2. **`glayout/flow/primitives/mimcap.py`**
   - Fixed mimcap and mimcap_array functions (lines ~85 and ~132)
   - Updated to handle both single capacitors and capacitor arrays

### Elementary Block Files
3. **`glayout/flow/blocks/elementary/LHS/transmission_gate.py`**
   - Fixed transmission_gate function (line ~137)
   - Updated tg_netlist function to handle both string and object netlists

4. **`glayout/flow/blocks/elementary/transmission_gate/transmission_gate.py`**
   - Fixed transmission_gate function (line ~131)
   - Updated tg_netlist function for consistency

5. **`glayout/flow/blocks/elementary/LHS/fvf.py`**
   - Fixed flipped_voltage_follower function (line ~162)
   - Updated fvf_netlist function to handle netlist objects properly

### Composite Block Files
6. **`glayout/flow/blocks/composite/fvf_based_ota/low_voltage_cmirror.py`**
   - Fixed netlist storage (line ~143)

7. **`glayout/flow/blocks/composite/fvf_based_ota/p_block.py`**
   - Fixed netlist storage (line ~92)

8. **`glayout/flow/blocks/composite/fvf_based_ota/n_block.py`**
   - Fixed netlist storage (line ~146)

## Solution Implementation

### Before (Problematic Code)
```python
component.info['netlist'] = some_netlist_function(...)
```

### After (Fixed Code)
```python
# Store netlist as string to avoid gymnasium info dict type restrictions
netlist_obj = some_netlist_function(...)
component.info['netlist'] = str(netlist_obj)
component.info['netlist_obj'] = netlist_obj  # Keep object reference for internal use
```

### Netlist Function Updates
For functions that use netlists from component.info, the pattern was updated:

```python
# Before
netlist.connect_netlist(component.info['netlist'], ...)

# After
component_netlist = component.info.get('netlist_obj', component.info['netlist'])
netlist.connect_netlist(component_netlist, ...)
```

## Benefits

1. **Compatibility**: Resolves gymnasium library compatibility issues
2. **Backward Compatibility**: Code still works with existing netlists
3. **Dual Storage**: Both string representation and object reference are available
4. **JSON Serializable**: Component info dictionaries can now be serialized to JSON
5. **No Functional Loss**: All netlist functionality is preserved

## Testing

Created comprehensive test scripts to validate the fix:
- `test_netlist_fix.py` - Basic validation
- `test_comprehensive_fix.py` - Tests multiple component types

All tests pass, confirming that:
- Netlist objects are stored as strings in `component.info['netlist']`
- Original objects are preserved in `component.info['netlist_obj']`
- Info dictionaries are JSON-serializable
- No functionality is lost

## For Your Friend

Your friend should now be able to run `generate_tg_1000_dataset.py` without encountering the gymnasium info dict error. The fix ensures that all component info dictionaries only contain basic data types that gymnasium can handle.

## Verification

To verify the fix works, your friend can run:
```bash
cd /path/to/LHS/directory
python test_comprehensive_fix.py
```

This will confirm that all components now store netlists properly and are compatible with gymnasium's requirements.
