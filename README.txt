# Programme d'acquisition des données i2c 

Ce programme python permet l'acquisition des données de deux capteurs i2c, un BME280 (température, humidité, pression atmosphérique) et un ICM20948 (accélérometre 3 axes, Gyroscope 3 axes, Magnétomètre 3 axes) sur un Raspberry Pi.

Le capteur BME280 est configuré avec son adresse i2c par défaut, soit 0x77
Le capteur ICM20948 est configuré avec son adresse i2c par défaut, soit 0x69

Les données collectées sont envoyées json sur le port UDP 5005 toutes les 10ms. Cette fréquence est nécessaire pour obtenir des données exploitables pour l'accéléromètre.

```json
{
  "temperature": 22.954804730558045,
  "humidity": 30.376441520141594,
  "pressure": 987.0626881398259,
  "gyroscope_x": 0.061068702290076333,
  "gyroscope_y": -0.16030534351145037,
  "gyroscope_z": 0.5801526717557252,
  "accelerometer_x": 0.0009765625,
  "accelerometer_y": -0.0048828125,
  "accelerometer_z": 1.021484375,
  "magnetometer_x": -18.75,
  "magnetometer_y": 32.55,
  "magnetometer_z": 61.05
}
```

## Installation du Script

### Prérequis

Identifiant et mot de passe du Raspberry

### Activation de l'i2c sur le Raspberry Pi

A l'aide d'un terminal, exécutez la commande raspi-config pour entrer dans le menu de configuration du Raspberry Pi

```shell
sudo raspi-config
```

Pour activer dans l'interface i2c dans raspi-config, il faut :

- sélectionner la ligne **3 Interface Options**
- sélectionner la ligne **sI5 I2C**
- répondre **Yes** à la question *"Would you like the ARM I2C interface to be enabled"
- sélectionner **Ok** pour terminer la configuration

### Instalation du programme sur le Raspberry Pi

L'installation du programme suit la procédure suivante:

1. Créer un dossier projection dans le dossier utilisateur `/home/<user>`
1. Copier les fichiers *read-all.py* et *requirements.txt* dans le dossier`/home/<user>/projection`
1. Créer un environnement de travail virtuel **venv**
   
	```shell
	cd projection
	python3 -m venv venv
	. venv/bin/activate
	pip3 install -r requirements.txt
	```
	
1. Créer un fichier `i2cdata.service` de service pour systemd dans le dossier `/etc/systemd/system`

	```service
	[Unit]
	Description=i2c sensor reader for projection box application

	[Service]
	User=pi
	WorkingDirectory=/home/pi/projection
	Restart=on-failure
	RestartSec=5s
	ExecStart=/home/pi/projection/bin/python3 -m i2c_data.py

	[Install]
	WantedBy=multi-user.target
	```
1. Démarrer le service avec la commande: suivantes pour démarrer et ajouter le service au démarrage du système

	```shell
	sudo systemctl start i2cdata.service
	```

1. Ajout le service au démarrage du Raspberry

	```shell
	sudo systemctl enable i2cdata.service
	```

  
