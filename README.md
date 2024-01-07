# ChatGuardians

link to [Sexism Dataset](https://huggingface.co/yangezheng) on HuggingFace



## Goal

This is a NLP project, the goal is to against sexism speech on internet, which can detect and perhaps generate counter speech.

### Problems we have encountered

1. Which model to use to detect a sexism speech?
2. Which model to use to generate counter speech?
3. After find the model, how should we deploy them so the users can use them?

### Answers to our problems

1. we are going to test many different models, which are pretrained with different goals, e.g. sentiment analysis. And see how different model performances.
2. to be found
3. we decided to go with Automat Chatbot, which will pull every messges from something like telegram channel, analyse it and send alert or counter speech.
