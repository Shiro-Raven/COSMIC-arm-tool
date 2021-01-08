# IWMS-MENSURA 2020: COSMIC Functional Size of ARM Assembly Programs [[Paper](http://ceur-ws.org/Vol-2725/paper1.pdf)]

This repo contains the source code of the prototype of the automated measurement tool mentioned in the published work. 

All measurements are based on the **Operation** pseudo-code present in the official ARM specification of their A32/T32 architecture, found [here](https://static.docs.arm.com/ddi0597/i/ISA_AArch32_xml_v87A-2020-09.pdf).

### Pre-requisites

  - Python (with tkinter installed)
  - An ARM (Cross) Compiler of your choice. An example of a cross-compiler is [this](https://www.acmesystems.it/arm9_toolchain).

### Usage (Linux)

  - Run ```gui.py```.
  - Select a file following the criteria mentioned in the paper.
  - Click ```Measure CFPs``` and inspect the results.
  - If you decide to save the results, the output will be saved in the ```out``` directory.

### TODO

- [ ] Make it optional to include native C headers from the measurement. 
- [ ] Complete the supported ARMasm list
- [ ] (Experimental) Use Regex to parse instructions more rigorously.

### Contact
If you face any problems using this tool, please create an issue, or get in touch with me through my [personal email](mailto:amfa.darwish.97@gmail.com).
If you find this repository useful for your research, please cite the following paper:
```
@inproceedings{Darwish2020COSMICFS,
  title={COSMIC Functional Size of ARM Assembly Programs},
  author={A. Darwish and Hassan Soubra},
  booktitle={IWSM-Mensura},
  year={2020}
}
```
