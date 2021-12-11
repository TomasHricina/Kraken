# Kraken Portfolio Viewer

Simple, effective way to inspect your Kraken portfolio

```
git clone git@github.com:TomasHricina/Kraken-Portfolio-Viewer.git   
cd Kraken-Portfolio-Viewer  
*Insert trades.csv from Kraken Web gui ( History -> Export )*
conda create -n kraken python=3.10.0 -y   
conda activate kraken   
pip install pandas    
pip install forex-python   
pip install pykrakenapi   
python main.py   
```

Limitations:   
Kraken does not export staking rewards, but the code tries to detect it anyways.    
