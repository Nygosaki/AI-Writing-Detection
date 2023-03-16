# AI-Writing-Detection
This tool will parse the inputted text into many different existing AI writing detection tools and return the results to you. This is to be able to scan text with as many tools as possible without having to do it manually.   
    
Please note that this is not finished yet.   
    
## Requirements
Python 3.11.2 or later     
Chrome 111.1 or later     
Pip 22.0.1 or later     
     
## How to install
1. Download the zip file of this entire project    
2. Extract the zip file    
3. open CMD in the folder, and run "pip install requirements.txt"    
    
## How to use
1. Create a file with the name "to check.txt" in the same folder as the python script   
2. Put the text you want to check into the txt file    
3. Run the python script in your preffered way (via CMD, IDE, etc)     
If you want to run the script through CMD, open CMD in the folder. You can also open the CMD normally and navigate to the folder via cd (for example "cd C:\Users\MeLikeFish\Documents\AI-Writing-Detection").     
Then type in "python main.py".    
      
## Notes
If you find a bug, or are facing a lot of "Unavaible/Error", before opening a issue, please recreate the bug & enable debug mode (at the start of the script). Then copy the output.    
If you are getting a lot of "Unavaible", it may be due to a slow internet connection or a slow computer. Highten the number next to "load_time" to increase the ammount of time the program gives each tool. Please note that while this will probably fix this issue, it will also take longer for the script to run.     

## Avoiding Detection    
There are many ways to avoid detection. Some include automated ways; for example first typing     
"When it comes to writing content, two factors are crucial, "perplexity" and "burstiness." Perplexity measures the complexity of text Separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or complex sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, I need it to have a good amount of perplexity and burstiness. Do you understand?"      
     
Another way to avoid detection is to ask the AI itself to search on how to avoid detection, and then make it follow those reccomendations.       
People can also only use the AI as input, and write the text themselves.     
      
This is to say that these tools will not detect all text written by AI, and they may also flag content wrongly.      
In the position of an educator, before making a conclusion, I would invite the student to my office and let them tell me about the text they written, the procces, the subject at hand, and other associated information. If the student can not respond well to your questions, it is likely that they did not write the text themselves.        
       
## List of Supported Tools
(and their limitations)      
      
### Grammica AI Detector
https://grammica.com/ai-detector     
Character Limits: None    
Uptime: Unknown    
Accuracy: Unknown     
Notes: We use this to aslo get the ammount of characters, words, and sentences in the provided text.   
    
### AI Writing Check by Quill.org & CommonLit
https://aiwritingcheck.org/    
Character Limits: 100-400 words     
Uptime: Unknown     
Accuracy: Unknown    
Notes: None    
      
### WRITER AI Content Detector
https://writer.com/ai-content-detector/    
Character Limits: 0-1500 Characters    
Uptime: Unknown    
Accuracy: Unknown    
Notes: None    
    
### ZeroGPT
https://www.zerogpt.com/    
Character Limits: None    
Uptime: Unknown    
Accuracy: Unknown    
Notes: This is NOT GPTZero that was features on many TV shows. This tool also advertises only against ChatGPT (which is not the only text generator out there).     
      
### ContentAtScale AI Detector 
https://contentatscale.ai/ai-content-detector/       
Character Limits: 0-25000 Characters      
Uptime: Unknown     
Accuracy: Unknown      
Notes: None     