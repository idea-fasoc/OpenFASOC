.. OpenFASOC documentation master file, created by
   sphinx-quickstart on Sun Jun  5 18:29:33 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OpenFASOC documentation!
==========================================
The OpenROAD (“Foundations and Realization of Open, Accessible Design”) project was launched in June 2018 within the DARPA IDEA program. OpenROAD aims to bring down the barriers of cost, expertise and unpredictability that currently block designers’ access to hardware implementation in advanced technologies. The project team (Qualcomm, Arm and multiple universities and partners, led by UC San Diego) is developing a fully autonomous, open-source tool chain for digital SoC layout generation, focusing on the RTL-to-GDSII phase of system-on-chip design. Thus, OpenROAD holistically attacks the multiple facets of today’s design cost crisis: engineering resources, design tool licenses, project schedule, and risk.

The IDEA program targets no-human-in-loop (NHIL) design, with 24-hour turnaround time and zero loss of power-performance-area (PPA) design quality.

The NHIL target requires tools to adapt and auto-tune successfully to flow completion, without (or, with minimal) human intervention. Machine intelligence augments human expertise through efficient modeling and prediction of flow and optimization outcomes throughout the synthesis, placement and routing process. This is complemented by development of metrics and machine learning infrastructure.

The 24-hour runtime target implies that problems must be strategically decomposed throughout the design process, with clustered and partitioned subproblems being solved and recomposed through intelligent distribution and management of computational resources. This ensures that the NHIL design optimization is performed within its available [threads * hours] “box” of resources. Decomposition that enables parallel and distributed search over cloud resources incurs a quality-of-results loss, but this is subsequently recovered through improved flow predictability and enhanced optimization.

For a technical description of the OpenROAD flow, please refer to our DAC-2019 paper: Toward an Open-Source Digital Flow: First Learnings from the OpenROAD Project. The paper is also available from ACM Digital Library. Other publications and presentations are linked here.

Code of conduct
----------------------
Please read our code of conduct here.

Documentation
----------------------



How to contribute
----------------------
If you are willing to contribute, see the Getting Involved section.

If you are a developer with EDA background, learn more about how you can use OpenROAD as the infrastructure for your tools in the Developer Guide section.

How to get in touch
----------------------
We maintain the following channels for communication:

Project homepage and news: https://theopenroadproject.org

Twitter: https://twitter.com/OpenROAD_EDA

Issues and bugs:

OpenROAD: https://github.com/idea-fasoc/OpenFASOC/issues

OpenROAD Flow: https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/issues

Discussions:

OpenROAD: https://github.com/The-OpenROAD-Project/OpenROAD/discussions

OpenROAD Flow: https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/discussions

Inquiries: openroad@eng.ucsd.edu

See also our FAQs.

.. toctree::
   :maxdepth: 8
   :caption: Contents


   code-of-conduct
   developers-guide
   README
   getting-started
   faqs
   contact
