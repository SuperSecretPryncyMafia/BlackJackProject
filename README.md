# BlackJackProject

## Training data 
As we consider a particular problem being a game against another player, not a dealer, our dataset would not be generated using this specific set of rules. After careful considerations, we came up with the following proposal of possible solutions:  
### The data format
current_sum -> (array if there are aces)
opponent_visible_card -> (array if there are aces)
opponent_card_no
player_card_no (may be of interest to the net, why not)
was_hit_okay_option (did we stay till next round)
### Random data generation
We decided to just generate the deck randomly and make random decisions for both players until one loses. However, it may be beneficial to store and generate the data as all the concurrent turns, because then the model can use both players' POVs for the game as two different samples. Therefore, for the generation only, it could be beneficial to just get the sequence of the cards and decisions for each of the players, stopping only after somebody loses. Then, in the next step, we could transform the data to be fit for the actual training.
### Make the model play against itself
