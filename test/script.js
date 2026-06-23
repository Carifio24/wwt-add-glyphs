let currentChoice = 1;

function createGlyphCache(choice) {
  if (choice == currentChoice) { return; }

  const cache = new wwtlib.GlyphCache();

  let spriteSheet = `glyphs${choice}.png`;
  let xmlSheet = `glyphs${choice}.xml`;
  if (choice == 1) {
    spriteSheet = wwtlib.URLHelpers.singleton.engineAssetUrl(spriteSheet);
    xmlSheet = wwtlib.URLHelpers.singleton.engineAssetUrl(xmlSheet);
  }
  
  cache._texture = wwtlib.Texture.fromUrl(spriteSheet);
  cache._webFile = new wwtlib.WebFile(xmlSheet);
  cache._webFile.onStateChange = cache._glyphXmlReady.bind(cache);
  cache._webFile.send();

  return cache;
}

function onWWTReady() {
  wwt = wwtlib.WWTControl.singleton;
  window.wwt = wwt;

  const settings = wwtlib.Settings.get_active();
  settings.set_showConstellationLabels(true);
}

function onLoad() {
  selector.addEventListener("change", event => {
    const choice = Number(event.target.value);
    const cache = createGlyphCache(choice);
    const namesBatch = wwtlib.Constellations._namesBatch;
    namesBatch._glyphCache = cache;
    namesBatch.prepareBatch();
  });

  const builder = new wwtlib.WWTControlBuilder("wwtcanvas");
  builder.startRenderLoop(true);
  const scriptInterface = builder.create(); 

  scriptInterface.add_ready(onWWTReady);
}

window.addEventListener("load", onLoad)
