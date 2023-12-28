# hack-ai-final
Stock Market Analysis and Prediction Agent: Develop an agent that analyzes stock market trends and predicts future movements. The agent should use historical data and current market indicators to provide insights and investment recommendations.

The following solution uses two agents which communicate with each other. One agent is responsible for getting the symbol of the company whose stock has to be analyzed. The other is responsible for taking that symbol and getting various paramenters related to those stocks and then reporting back wheter it is a good investment or not 

To run the program

``git clone https://github.com/JimmyDogfish/hack-ai-final.git``
  
``cd hack-ai-final``

Change the blank API field in src/agents/config.py

``poetry install``

``poetry shell``

``python3 src/agents/ml_agent.py``

Open another terminal/command prompt 

``poetry shell``
``python3 src/agents/agents/main_agent.py``

Then just follow steps and use it!
