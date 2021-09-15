# Make Circles

Take a csv input and output a kml file with radius circles plotted around each point

The .csv input should have at least the following columns:
- latitude
- longitude
- accuracy_radius

## Usage
```bash
$ python3 make_circles.py -i input.csv -o output.kml
```

## Output
By loading the kml output into Google Earth will produce something akin to the following
![circles](https://github.com/cybercdh/make-circles/blob/media/circles.png?raw=true)

Light and thin circles denote wide radii, whilst thick, red circles are more accurate.

## Contributing
Pull requests are welcome. 

For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)