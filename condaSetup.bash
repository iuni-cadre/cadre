conda info --envs
conda create -y -p /home/jovyan/ISSItutorial/conda python=3.7 
source /opt/conda/etc/profile.d/conda.sh
conda activate /home/jovyan/ISSItutorial/conda

conda install -c conda-forge wordcloud
conda install -c conda-forge pandas
conda install -c conda-forge matplotlib
conda install -c conda-forge nltk 
pip install python-igraph --user
pip show python-igraph
cp -r ~/.local/lib/python3.7 ~/ISSItutorial/local/lib/python3.7
