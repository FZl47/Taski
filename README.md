# Taski

## TODO
- [ ] Refactor name views and swagger
- [ ] Set Swagger views in "swagger.py" file (task,account) apps
- [ ] Inherit all serializer from "core.serializers.BaseSerializer"
- [ ] Refactor Serializers  
- [ ] Remove some query param from urls(shorten) 
- [ ] Fix all routes action by method (not name)
  - items:GET &#9745;
  - items-get:GET &#x2612;


## DRF-YASG
### Add some style in template redoc(Fix Bug)
_Added some style to template redoc(drf-yasg)
for Fix some bug in template(**venv/Lib/site-packages/drf_yasg/templates/drf_yasg/redoc.html**)_
```css
    .sc-dTSzeu.jlrIPb + div .sc-TtZnY.sc-jHNicF.ehnWxS.imjMKL{
        display:None;
    } 
```
### Add some style in template redoc(better UI)
```css
    .sc-fujyAs.kreCXJ{
            text-align: center;
            color: #42238c;
            background: rgba(249, 250, 252, 0.8);
            padding: 10px;
            font-size: 200%;
            border-radius: 10px;
    }
```

