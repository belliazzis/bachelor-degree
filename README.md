# 3D SAR Tomography Reconstruction in Urban Environments

This repository contains the code and experiments that are part of my Bachelor's thesis, **"Techniques for 3D SAR Tomography in Urban Environments"**, ehich objective was to compares different techniques for reconstructing the **vertical reflectivity profile** of urban scenes from multi-baseline Synthetic Aperture Radar (SAR) data.

The reconstruction methods considered are:

- **Singular Value Decomposition (SVD)**
- **Beamforming**
- **Compressive Sensing (CS)**
- **Complex-valued Neural Network**


---

## Project Overview

SAR tomography allows the reconstruction of the vertical distribution of radar scatterers by using SAR acquisitions from different observation geometries.

The main objective of this project is to investigate the capabilities and limitations of different reconstruction approaches

The experiments were designed in two stages:

1. **Simulated data**, where the scene geometry and target positions are known;
2. **Real SAR data**, where the techniques are applied to a multi-baseline dataset of an urban environment, specifically a real SAR dataset of **Piazza del Plebiscito, Naples, Italy**.

---

## Reconstruction Methods

### 1. SVD

The Singular Value Decomposition approach uses the pseudo-inverse of the steering matrix to solve the inverse reconstruction problem.

It provides a direct and computationally efficient solution, but its performance can be affected by noise and limited vertical resolution.

### 2. Beamforming

Beamforming is a computationally simple reconstruction technique based on projecting the observed data along the directions described by the steering matrix.

Although fast and easy to implement, it generally provides lower vertical resolution and less precise separation of nearby scatterers.

### 3. Compressive Sensing

Compressive Sensing is based on the assumption that the vertical reflectivity profile is sparse.

The method searches for a sparse solution compatible with the observed SAR measurements and can provide sharper reconstructions than conventional approaches, at the cost of higher computational complexity.

### 4. Complex-valued Neural Network

A two-layer neural network implemented in **Python using the PyTorch framework** was used as a learning-based reconstruction approach.

The network operates on complex-valued SAR data and was trained to estimate the complex reflectivity vector.

Different initializations were investigated, including:

- zero initialization;
- initialization using SVD reconstruction;
- initialization using Beamforming reconstruction;
- initialization using Compressive Sensing reconstruction.

---

## Experiments on Simulated Data

The first stage of the project uses simulated generated SAR data simulated in MATLAB.

A simplified scenario containing two point-like scatterers at different heights is considered. The vertical distance between the targets is varied in order to evaluate the resolution capabilities of the different reconstruction methods.

The experiments investigate:

- closely spaced targets;
- vertically separated targets;
- different reconstruction initializations;
- the effect of the Signal-to-Noise Ratio (SNR);
- the behavior of the neural network when initialized from conventional reconstruction methods.

Because the ground-truth reflectivity profile is known, the reconstructed profiles can be directly compared with the original scene.

The simulations show that the separation between targets has a great influence on reconstruction quality, the neural network performs better when the targets are more clearly separated.

The experiments also show an interesting behavior in low-SNR conditions, where the neural network is able to preserve the location of the targets while reducing some of the noise and spurious peaks observed in the conventional reconstructions.

---

## Experiments on Real SAR Data

The second stage applies the reconstruction techniques to a real multi-baseline SAR dataset of **Piazza del Plebiscito in Naples, Italy**.

The dataset consists of **27 SAR acquisitions obtained from slightly different geometries**, which provide the geometric diversity required for tomographic reconstruction.

The urban environment represents a challenging scenario because of:

- complex architectural structures;
- multiple scattering mechanisms;
- layover;
- shadowing;
- speckle noise;
- multiple scatterers within the same ground-resolution cell.

For the real-data experiments, the MATLAB implementation was adapted to process the complete dataset pixel by pixel and generate **height maps** from the reconstructed vertical profiles.

Both unfiltered and median-filtered reconstructions are produced.

---

## Software and Technologies

The project was developed using:

- **MATLAB** – SAR simulation, conventional reconstruction methods and real-data processing;
- **Python** – neural-network implementation;
- **PyTorch** – training and inference of the neural network;
- **NumPy / SciPy** – numerical processing and data manipulation;
- **MAT-files** – exchange of data between MATLAB and Python.

The MATLAB and Python implementations are used together: MATLAB is primarily employed for SAR data generation and conventional reconstruction, while Python/PyTorch is used for the learning-based approach. 

---

## Results

The experiments highlight different strengths and limitations of the investigated approaches.

For simulated data:

- **Beamforming** is simple and fast but provides relatively low resolution.
- **SVD** provides improved localization but remains sensitive to noise.
- **Compressive Sensing** generally produces sharper and more accurate reconstructions by exploiting scene sparsity.
- The **neural network** can reconstruct the general structure of the scene and shows promising behavior, particularly in noisy scenarios.

For real SAR data, Compressive Sensing provides the best reconstruction among the conventional MATLAB-based methods. The combination of **Compressive Sensing and neural-network reconstruction**, followed by median filtering, produced the most accurate and visually clean height map among the tested approaches. 

An important limitation is represented by **shadowed areas**. Since the radar signal cannot reach these regions, the available measurements do not contain sufficient information to reliably estimate their elevation. Consequently, all reconstruction methods produce unreliable values in these areas.

---

## Repository Structure

---

## Data Availability

The repository contains the code used to perform the experiments and generate the presented results.

---

## Thesis

This repository accompanies the Bachelor's thesis:

**"Techniques for 3D SAR Tomography in Urban Environments"**

Bachelor's Degree in Computer, Biomedical and Telecommunications Engineering (L-8)

---

## Author

**Sonia Belliazzi**

Bachelor's Degree in Computer, Biomedical and Telecommunications Engineering

This repository is intended primarily for academic and research purposes.

If you use or adapt this code, please cite the corresponding thesis.
