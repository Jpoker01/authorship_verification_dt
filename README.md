# Authorship verification using chosen artificial intelligence methods

This project folder includes all the work performed in scope of the diploma thesis 'Authorship verification using chosen artificial intelligence methods'.  
The final deployed website can be accesed through: <LINK_TO_BE_ADDED>  
The diploma thesis (in Czech) is available at: <LINK_TO_BE_ADDED>  

## Project structure

The work can be broken to two main parts:
* **Experiments** - All of the jupyter notebooks where different methods of AI are utilized and experimented with to find the optimal solution
* **Web application** - The web application where a chosen authorship verification model is deployed and where the user can verify authorship of two texts.

#### Experiments
Lists all the experiments done for this diploma thesis.

* **/experiments** - lists all experiments
   * **requirements.txt** - The requirements for reproducing the implementation environment
   * **/conf** - Space for configurations
       * **/base** - Shared configuration like parameters
       * **/local** - Local configurations such as credentials
   * **/notebooks** - Jupyter notebooks - naming convention "YYYYMMDD_developerinitials - description"
     * **/dataset** - Notebooks related to dataset processing and exploration
     * **/graph** - Notebooks related to experiments utilizing integrated syntactic graphs
     * **/llm** - Notebooks utilizing LLMs
     * **/traditional** - Notebooks utilizing traditional BOW/TF-IDF representations for experiments 
     * **/transformer** - Notebooks utilizing transformer based models for experiments
   * **/results** - Final analysis documents
     * **/llm** - Lists all the LLM experiment results (used before utilizing MLFlow)
     * **/prilohaC_MLFlow_all_experiments_export.xlsx** - Lists all the MLFlow results for other experiments
     
####  Web application
Contains the source code for the frontend and backend of the final web application solution

* **/webapp**
  * **/frontend** - Contains the source code for the frontend of the web application
  * **/backend** - Contains the source code for the backend of the web application
