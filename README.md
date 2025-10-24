# Everything-Political-Compass

## Goal:
### Create an interactive map showing where any public entity sits on a globally scaled political compass.
*With minimal human input and with the widest scope.*

## Challenges:
### Privacy & Ethics: 🤪
### Biases and inaccuracies:


## Python Analysis:
- Creating a polical compass graph, that automatically shows any public figure we enter on the classic left-right, auth-lib plane.
- This will use sets of questions on every political topic in the world and have an LLM answer the question on a -1 to +1 scale.
- To make sure there is no bias further prompting can be made to ensure it is considering -1 to be the most anti take in the whole world vs +1 which would be the most pro take in the whole world.
- Then we can use those numbers to somehow place them on a graph.

## Contributers:
- AutumnSear
- thezwarteridder



## Quick start:
Before trying anything, clone the repo and run 
`pip install -r Everything-Political-Compass\requirements.txt`

### Mapping and analysing:
1. The data is already all in the data folder so you can do what you want with it.
2. you can run `manual.py` to get a graph and interface.

### Generating new data for new entities
*Wont be quick but it'll be a start..*
Keep in mind this will require a somewhat alright computer.
1. First you will want to get [Ollama](https://ollama.com/).
2. Download a model (I use "gpt-oss:20b" but you can use whatever so long as you change the model variable in `main.py`).
3. Test that the model you downloaded works in the ollama GUI.
4. Run `main.py` with the entities list filled with any entity you want to be generated.

