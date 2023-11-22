# GenBot: Generative Simulation Empowers Automated Robotic Skill Learning at Scale


---

This is the code for the paper:
GenBot: Generative Simulation Empowers Automated Robotic Skill Learning at Scale

This repo contains a re-implementation of GenBot using PyBullet, containing generation and learning of rigid manipulation and locomotion tasks. Our full pipeline containing soft-body manipulation and more tasks will be released later together with Genesis.


## Setup
### GenBot
Clone this git repo.
```
git clone https://github.com/GenerativeSimulation/GenBot.git
```
We recommend working with a conda environment.
```
conda env create -f environment.yaml
conda activate GenBot
```
If installing from this yaml file doesn't work, manual installation of missing packages should also work.

### Open Motion Planning Library
GenBot leverages [Open Motion Planning Library (OMPL)](https://ompl.kavrakilab.org/) for motion planning as part of the pipeline to solve the generated task. 
To install OMPL, run
```
./install_ompl_1.5.2.sh --python
```
which will install the ompl with system-wide python. Then, export the installation to the conda environment to be used with GenBot:
```
echo "path_to_your_ompl_installation_from_last_step/OMPL/ompl-1.5.2/py-bindings" >> ~/miniconda3/envs/GenBot/lib/python3.9/site-packages/ompl.pth
```
remember to change the path to be your ompl installed path and conda environment path.


### Dataset
GenBot uses [PartNet-Mobility](https://sapien.ucsd.edu/browse) for task generation and scene population. We provide a parsed version [here](https://drive.google.com/file/d/1JR9NyHrJCROyEQ0IHqyI0rp2T9b6sN_Z/view?usp=sharing) (which parses the urdf to extract the articulation tree as a shortened input to GPT-4). After downloading, please unzip it and put it in the `data` folder, so it looks like `data/dataset`.

For retrieving objects from objaverse, we embed object descriptions from objaverse using [SentenceBert](https://www.sbert.net/). 
If you want to generate these embeddings by yourself, run
```
python objaverse_utils/embed_all_annotations.py
python objaverse_utils/embed_cap3d.py
python objaverse_utils/embed_partnet_annotations.py
```


## Run GenBot
### Generate tasks and perform skill learning
Put your OpenAI API key at the top of `gpt_4/query.py`, and simply run
```
source prepare.sh
python run.py
``` 
GenBot will then generate the task, build the scene in pybullet, and solve it to learn the corresponding skill.  
If you wish to generate manipulation tasks relevant to a specific object, e.g., microwave, you can run  
```
python run.py --category Microwave
```

### Generate tasks
If you wish to just generate the tasks, run
```
python run.py --train 0
```
which will generate the tasks, scene config yaml files, and training supervisions. The generated tasks will be stored at `data/generated_tasks_release/`.  
If you want to generate task given a text description, you can run
```
python gpt_4/prompts/prompt_from_description.py --task_description [TASK_DESCRIPTION] --object [PARTNET_ARTICULATION_OBJECT_CATEGORY]
``` 
For example,
```
python gpt_4/prompts/prompt_from_description.py --task_description "Put a pen into the box" --object "Box"
```

### Learn skills
If you wish to just learn the skill with a generated task, run
```
python execute.py --task_config_path [PATH_TO_THE_GENERATED_TASK_CONFIG] # for manipulation tasks
python execute_locomotion.py --task_config_path [PATH_TO_THE_GENERATED_TASK_CONFIG] # for locomotion tasks
```
For example,
```
python execute.py --task_config_path example_tasks/Change_Lamp_Direction/Change_Lamp_Direction_The_robotic_arm_will_alter_the_lamps_light_direction_by_manipulating_the_lamps_head.yaml  
python execute_locomotion.py --task_config_path example_tasks/task_Turn_right/Turn_right.yaml
```

### Pre-generated tasks
In `example_tasks` we include a number of generated tasks from GenBot. We hope this could be useful for, e.g., language conditioned multi-task learning & transfer learning & low-level skill learning. We hope to keep updating the list! 

## Acknowledgements
- The interface between OMPL and pybullet is based on [pybullet_ompl](https://github.com/lyfkyle/pybullet_ompl).
- Part of the objaverse annotations are from [Scalable 3D Captioning with Pretrained Models](https://arxiv.org/abs/2306.07279)


