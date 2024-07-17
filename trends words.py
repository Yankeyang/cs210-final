import pandas as pd
data = {
    "Year": [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "Words": [
        "Austerity,App,Big Society,Spillcam,Vuvuzela",
        "Occupy,Squeezed Middle,Crowdsourcing,Hacktivist,Arab Spring",
        "GIF,YOLO,Omnishambles,Eurogeddon,Superstorm",
        "Selfie,Twerk,Bitcoin,Binge-watch,Showrooming",
        "Vape,Bae,Photobomb,Normcore,Slacktivism",
        "Face with Tears of Joy,Lumbersexual,Dark Web,Refugee,Ad Blocker",
        "Post-truth,Brexit,Hygge,Chatbot,Adulting",
        "Feminism,Fake News,Inaugurate,Recuse,Empathy",
        "Justice,Toxic,Techlash,Lodestar,Gammon",
        "They,Climate Emergency,Cancel Culture,Influencer,Nonbinary",
        "Pandemic,Lockdown,BLM,Social Distancing,Flatten the Curve",
        "Vaccine,Insurrection,NFT,Supply Chain,WFH",
        "Gaslighting,Metaverse,#IStandWith,Goblin Mode,Wordle"
    ]
}
df = pd.DataFrame(data)
df.to_csv('trendingwords.csv', index=False)
print("trendingwords.csv")