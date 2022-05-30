# dash-docset-jax

![screenshot](/screenshot.jpg)

View JAX docs in the [dash](https://kapeli.com/dash)/[zeal](https://github.com/zealdocs/zeal) offline docset browser.

To use, you can add this feed in Dash/Zeal:
```
https://raw.githubusercontent.com/ppwwyyxx/dash-docset-jax/master/Jax.xml
```
Or download the latest release [here](https://github.com/ppwwyyxx/dash-docset-jax/releases).


## Steps to generate the docset

1. `pip install tqdm python-magic selectolax doc2dash beautifulsoup4 lxml`
2. Build JAX documentation following its [official instructions](https://jax.readthedocs.io/en/latest/developer.html#update-documentation)
   and save results under `original-docs` (equivalent to `docs/build/html` under jax).
3. Preprocess the HTMLs: `./transform.py original-docs`
4. Fix the CSS: `sed -i 's/var(--pst-font-family-monospace)/monospace/g' original-docs/**/*.css`
5. Generate the docset:
   ```
   doc2dash -d ./ --online-redirect-url https://jax.readthedocs.io/ --name jax original-docs
   ```
   This will generate `jax.docset` that can be installed into Zeal/Dash.
