# A tool for visualizing data from a heating system with a wood-burning boiler.
For now, this repo is just a helper for visualizing the sensor data I collected with my Atmega controller based RF sensor acquisition system and 433MHz RF radio modules that I built from scratch back in 2015 to investigate how a boiler works on firewood. I had sensors for supply, return, firewood door where firewood was loaded, and a sensor in one of the heated rooms. I also installed one sensor outside, but it refused to work in temperatures under 0 degrees Celsius. It was probably a battery issue. So I decided to take the outdoor temperature from the weather server API for my city. You can see this code [here](https://github.com/kozak-yakym/visualisation_tool/tree/main/Python/DCS)         
That time, I had just started learning Python and didn't know how to visualize there. So I simply saved the data to several files. And only in 2020, I decided to apply my new knowledge in Python to analyze data visually.          
     
You can see the result of the visualizer on my page: [https://kozak-yakym.github.io/](https://kozak-yakym.github.io/graph.html)    
         
This Pet project is still under development. Below are some things I would like to see improved.
I need:
* Think about modularity
* Consider refactoring
* Replace magic numbers with macros or constants
* Add documentation to Readme. At least more information about the architecture of my data collection system
* Add parameters to Python script execution
    - Enable/disable file generation
    - Enable/disable graph drawing
    - Change file names to other ones
    - Enable/disable all features above
* It is also necessary to work on the data collector of the RF DataCollecting system
    - There are some examples of UART work and the Weather API that I used. I think there is a huge room for improvement
    - Create a data generator based on the data collector to test the entire system
* Plans for the distant future
    - Add code reliability. Come up with something to prevent the code from crashing if, for example, there is no log file.
    - Add live view to collection system. Of course there are more successful architectures and maybe you should switch to something other than Python. But I would still try it in Python to learn more about its capabilities

