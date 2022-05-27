Real Time ML trading BOT

Developing this to learn more about applying ML to real-time trading strategies. 
In future I plan to add other sources of data such as:
  + Sentiment (Twitter/articles)
  + On-chain analytics
  + Specific wallet movements (whales moving crypto around)

Currently just gathering test/train/validation data for creating an algorithm.

Idea: 
  + LOB tells us in the short term what investors are thinking:
    + Is there a large sell wall close to the market price?
    + Have a lot of bids been placed in the last 30 seconds?
    + Were lots of cancellations just made on a particular side?
  + On short enough time frames can this be used to quickly enter and exit trades?

Learning Phase:
  + Gathers level 2 LOB data using the Coinbase Pro API
  + Generalises LOB curves to a set of discrete 'feature points'
  + Future market price will be to train the ML model based on the feature set
