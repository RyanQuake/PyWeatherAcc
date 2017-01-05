# PyWeatherAcc
<paragraph> The purpose of this project is to get a feeling which accuracy several weather services are providing. Therefore the following tools/languages where used:</paragraph> 
<ul>
  <li>Python: Programming language of choice</li>
  <li>MySQL: Used to store data objects</li>
  <li>JSON: data object layout of choice</li>
</ul> 

<h2> supported weather services </h2>
<ul>
  <li>OpenWeatherMap (http://openweathermap.org/)</li>
  <li>Weather Underground (https://www.wunderground.com/)</li>
</ul> 

<h2> How to use </h2>
<ol>
  <li>Clone repository.</li>
  <li>Create a config.ini file according to config.ini_example.
    <ul>
      <li>This may include to register at the weather services.</li>
    </ul>
  </li>
  <li>Run 'python updateDB.py' in /bin/</li>
</ol>

<h2> Features planned </h2>
<ul>
  <li>dynamic recognition, which weather services to use</li>
  <li>rework the handling of the config file</li>
  <li>adding support for more weather services</li>
  <li>engine for data analysis</li>
</ul> 

<h2> Version History </h2>
<h4> 0.2.1 </h4>
added support for Weather Underground, reworked handling to query and commit data
<h4> 0.2.0 </h4>
changed storing concept, to store json object
<h4> 0.1.0 </h4>
basic concept implementation, support for OpenWeatherMap

<h6> Keywords </h6>
<small>python, git, github, weather, accuracy, mysql, sql, api, data analysis, raw data</small>
