## JAX+Flax offline documentation in [dash](https://kapeli.com/dash)/[zeal](https://github.com/zealdocs/zeal) docset browser

![screenshot](/screenshot.jpg)

To use, you can add this feed in Dash/Zeal directly:
```
https://raw.githubusercontent.com/ppwwyyxx/dash-docset-jax/master/Jax.xml
```
Or download the latest release [here](https://github.com/ppwwyyxx/dash-docset-jax/releases).


## Steps to generate the docset

1. Install JAX and Flax
1. `pip install tqdm python-magic selectolax doc2dash beautifulsoup4 lxml`
1. Build their documentation together:
   ```
   git clone https://github.com/google/jax /tmp/jax
   git clone https://github.com/google/flax /tmp/flax

   cd /tmp/flax/docs/
   # Install necessary doc dependencies from requirements.txt, then:
   sphinx-build -b html -D nb_execution_mode=off ./ ./build/html -j auto

   cd /tmp/jax/docs
   cp -rv /tmp/flax/docs/api_reference/flax.* ./
   # Install necessary doc dependencies from requirements.txt, then:
   sphinx-build -b html -D nb_execution_mode=off ./ ./build/html -j auto
   ```
1. `cd` to this project, then run the following to beautify the docs:
   ```
   export HTML_DIR=/tmp/jax/docs/build/html
   # Beautify the docs for more friendly display:
   ./transform.py $HTML_DIR
   # Use monospace font for code:
   sed -i 's/var(--pst-font-family-monospace)/monospace/g' $HTML_DIR/**/*.css
   doc2dash -f -d ./ -u https://jax.readthedocs.io/ --name jax -i icon.png $HTML_DIR
   ```
   This will generate `jax.docset` that can be installed into Zeal/Dash.


## Others

* Latex renders correctly:

![math](/math.jpg)

* Syntax highlight works (check `flax.linen.map_variables`)
