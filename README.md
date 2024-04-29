# esports-mathematics
Resources for combination video games and esports with mathematical pedagogy.

## Battle Royale Model

```
streamlit run main.py
```

## Requirements

```
conda env export --from-history > environment.yml # generate environment.yml 
conda env create -f environment.yml # create new conda environment from environment.yml
```


## Issues

### Battle Royale Model
- Map is drawn upside down
- Need cleaner control logic in the streamlit frontend
- Need to add stats & killcount to plot
- Need to add final scores as last frame
- Add option to save animation to file 

Note: if we are happy displaying the animation in a matplotlib window (and running the simulation from command line / from Python IDE) then it can render effectively instantly.
The issue comes when we want an interactive frontend too, in which case we have to pay a couple seconds' penalty to render the animation.