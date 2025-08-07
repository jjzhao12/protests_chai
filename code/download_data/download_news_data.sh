#!/bin/bash
#SBATCH --job-name=downloadimage
#SBATCH --account=juliame0
#SBATCH --partition=standard
#SBATCH --time=04-00:00:00
#SBATCH --mem=4gb
#SBATCH --mail-type=BEGIN,END,FAIL

python download_image_data.py

