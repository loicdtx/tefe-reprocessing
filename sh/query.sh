#!/bin/bash

lsru login
lsru sp_order --collection LT5 --xmin -65.2 --xmax -64.6 --ymin -3.8 --ymax -3.1 --start_date 1980-01-01 --proj aea --resize
lsru sp_order --collection LE7 --xmin -65.2 --xmax -64.6 --ymin -3.8 --ymax -3.1 --start_date 1998-01-01 --proj aea --resize
lsru sp_order --collection LC8 --xmin -65.2 --xmax -64.6 --ymin -3.8 --ymax -3.1 --start_date 1980-01-01 --proj aea --resize