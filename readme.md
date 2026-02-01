# How to get started
Clone this repo - `git clone https://github.com/peterbarraud/the-cricket-test.git'
Copy the following files to these locations
* [Config.json](https://drive.google.com/file/d/1T_o6gyqPoIPZ51k9TIXOHnWHSleNBLSi/view?usp=drive_link) to the libs folder 
* [game.jsons](https://drive.google.com/file/d/1JdBrp1tSPfPzNmo3BFl3-25c58qfQSCz/view?usp=drive_link) - extract the zip to the data folder - make sure the folder name is `games.jsons` (and it's under the `data` folder). And it directly contains the `game.json` files

* [series.soups](https://drive.google.com/file/d/1JdBrp1tSPfPzNmo3BFl3-25c58qfQSCz/view?usp=drive_link) - extract the zip to the data folder - make sure the folder name is `series.soups` (and it's under the `data` folder). And it directly contains the `series.soup` files


## Get dataframe by CSV
Use the `get_dataframe_by_name`

## Epoch time to datetime
We are saving start and end date of a match in epoch time (instead of datetime). so, you'll need to extract datetime out if you want a pretty looking date
But sorting of games by date, might actually be more efficient this way
```
from datetime import datetime
dt = datetime.fromtimestamp(epoch)
# for negative epoch (seems to be specifically required for Windows OS)
dt = datetime(1970, 1, 1) + timedelta(seconds=-2928441600)
```


