# BlackJackProject

## Data 
As we consider a particular problem being a game against another player, not a dealer, our dataset would not be generated using this specific set of rules. After careful considerations, we came up with the following proposal of possible solutions:  
### The data format
- current_sum -> (array if there are aces)
- opponent_visible_card -> (array if there are aces)
- player_card_no (may be of interest to the net, why not)
- opponent_card_no
- decision (if we stayed till next round, then the one taken, otherwise the other one) -> ground truth  
The last one should probably be this way or we have to find something to penalize the stand as a single decision. But maybe we should so that the model doesn't get saturated during playing against itself - then both will just stand forever.

### Random data generation
We decided to just generate the deck randomly and make random decision for the opponent until one loses. It would be beneficial to store and generate the data as all the concurrent turns, because then the model can use both players' POVs for the game as two different samples. Therefore, for the generation only, it could be beneficial to just get the sequence of the cards and decisions for each of the players, stopping only after somebody loses. Then, in the next step, we could transform the data to be fit for the actual training.

### Make the model play against itself
As the player will not make decisions randomly, we need to do something to simulate actual competition between the participants. To do so, the idea is to generate several decks of cards that will not change between the reruns in the training. Then, the model will be asked to make decisions for both sides and this way the data will be generated.

### Data for finetuning 
To actually train the model to compete with humans, we will run a few games against an actual player. Then, the data will be used to finetune the network.

### What to do with the aces
As shown before, we get the arrays of the current sum if aces occur. We decided that each of the cases should be considered separately and then the best possible choice should be made based on each of the predictions. Intuition suggests that the moves proposed by smaller sums should be more meaningful than for like, two aces and 20 because of it. I would propose a small dense layer with like one neuron that would find the best ratio that would be finetuned during games aginst itself and players. But then, it would have to be split into the cases:
- 1 A & 0 A, 0 A & 1 A - 2 cases to consider
- 1 A & 1 A - 4 cases 
- 2 A & 0 A - 3 cases 
- 2 A & 1 A - 6 cases,  
so it may be better to just leave it as a simple mean.

## Model
