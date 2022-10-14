# BlackJackProject

## Data 
As we consider a particular problem being a game against another player, not a dealer, our dataset would not be generated using this specific set of rules. After careful considerations, we came up with the following proposal of possible solutions:  
### The data format
- current_sum -> (array if there are aces)
- opponent_visible_card -> (array if there are aces)
- opponent_card_no
- player_card_no (may be of interest to the net, why not)
- was_hit_okay_option (did we stay till next round) -> ground truth  
The last one should probably be this way or we have to find something to penalize the stand as a single decision. But maybe we should so that the model doesn't get saturated during playing against itself - then both will just stand forever.

### Random data generation
We decided to just generate the deck randomly and make random decision for the opponent until one loses. Then, we have options: 
1. As the point of the training is to check if the model should hit, we probably should make it hit every time in the random data and then check if it made us lose - naive approach as the starting point?  (please correct me if i'm wrong and the random would overally be better or if we should mix.)
2. However, it may also be beneficial to store and generate the data as all the concurrent turns, because then the model can use both players' POVs for the game as two different samples. Therefore, for the generation only, it could be beneficial to just get the sequence of the cards and decisions for each of the players, stopping only after somebody loses. Then, in the next step, we could transform the data to be fit for the actual training. However, we have no way to decide if staying was a good option if we lose - maybe the chance to lose if we took the card was too high either way, i.e. for two cards having sum of ten, it would be stupid to hit, so it's possible that the best course of action is to stand and hope that the opponent will overhit rather than win.

### Make the model play against itself
As the player will not make decisions randomly, we need to do something to simulate actual competition between the participants. To do so, the idea is to generate several decks of cards that will not change between the reruns in the training. Then, the model will be asked to make decisions for both sides and this way the data will be generated. In this case, we will be focusing more on the 

### Data for finetuning 
To actually train the model to compete with humans, we will run a few games against an actual player. Then, the data will be used to finetune the network.

### What to do with the aces
As shown before, we get the arrays of the current sum if aces occur. We decided that each of the cases should be considered separately and then the best possible choice should be made based on each of the predictions. Intuition suggests that the moves proposed by smaller sums should be more meaningful than for like, two aces and 20 because of it. I would propose a small dense layer with like one neuron that would find the best ratio that would be finetuned during games aginst itself and players.

## Model
