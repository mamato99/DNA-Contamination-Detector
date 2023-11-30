# DNA Contamination Detector

## Description
This Python project addresses the issue of DNA contamination during laboratory processes. It identifies contaminants in a DNA string (`s`) by comparing it to a set of known contaminants (`C`). The degree of contamination is determined by the number of maximal substrings of a contaminant that exceed a specified contamination threshold (`l`).

## Class: DNAContamination

### Methods

#### `DNAContamination(s, l)`
- **Description:** Initializes a DNAContamination object.
- **Input:**
  - `s` (str): The DNA string to be verified.
  - `l` (int): The contamination threshold.
- **Output:**
  - None

#### `addContaminant(c)`
- **Description:** Adds a contaminant to the set `C` and saves the degree of contamination of `s` by `c`.
- **Input:**
  - `c` (str): Contaminant string.
- **Output:**
  - None

#### `getContaminants(k)`
- **Description:** Returns the `k` contaminants with the highest degree of contamination among the added contaminants.
- **Input:**
  - `k` (int): The number of contaminants to retrieve.
- **Output:**
  - List of `k` contaminants.

### Time Complexity Requirements

- `addContaminant(c)`: O((len(s) + len(c))² + log m), where `m` is the total number of contaminants.
- `getContaminants(k)`: O(k log m)

## Function: `test`

### Description

A function named `test(s, k, l)` reads DNA strings from the dataset `target_batcha.fasta` and returns the indices of the `k` contaminants in the dataset with a higher degree of contamination in `s`, assuming `l` as the contamination threshold. The function returns a string containing these indices in increasing order, separated by comma and space.

### Input

- `s` (str): The DNA string to be verified.
- `k` (int): The number of contaminants to retrieve.
- `l` (int): The contamination threshold.

### Output

- String containing the indices of contaminants.
