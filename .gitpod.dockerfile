FROM gitpod/workspace-full

# install and activate python 3.12
RUN pyenv update && pyenv install 3.12 && pyenv global 3.12