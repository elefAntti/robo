# robo

kinematics code for a differential drive robot and an ui to test it.

## You need
rxpy: pip install rx

qt5: pip install pyqt5

## valheen venvi ohje

Siis luo kansio projektille. Luo venv komennolla

python3 -m venv venv

Aktivoi venv komennolla


source venv/bin/activate

Tee koodia. Lataile tarvittavia paketteja. Sit aja


pip freeze > requirements.txt

Laita .gitignore:een venv

Laita githubiin.

Sit joku kloonaa sen githubista. Sit se ajaa siinä repossa noi samat komennot, paitsi ei tota freezeä. Sen sijaan se ajaa

pip install -r requirements.txt
