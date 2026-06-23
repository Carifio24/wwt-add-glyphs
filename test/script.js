let currentChoice = 1;

function updateGlyphs(choice) {
  if (choice == currentChoice) { return; }

  const cache = wwtlib.GlyphCache;

  cache.cleanUpAll();
  let spriteSheet = `glyphs${choice}.png`;
  let xmlSheet = `glyphs${choice}.xml`;
  if (choice == 1) {
    spriteSheet = wwtlib.URLHelpers.singleton.engineAssetUrl(spriteSheet);
    xmlSheet = wwtlib.URLHelpers.singleton.engineAssetUrl(xmlSheet);
  }
  
  cache._texture = wwtlib.Texture.fromUrl(spriteSheet);
  cache._webFile = new wwtlib.WebFile(spriteSheet);
  cache._webFile.onStateChange = cache._glyphXmlReady.bind(cache);
  cache._webFile.send();
}

function onWWTReady() {
  wwt = wwtlib.WWTControl.singleton;
  window.wwt = wwt;

  const settings = wwtlib.Settings.get_active();
  settings.set_showConstellationLabels(true);
}

function onLoad() {
  selector.addEventListener("input", event => {
    const choice = Number(event.data);
    updateGlyphs(choice);
  });

  const builder = new wwtlib.WWTControlBuilder("wwtcanvas");
  builder.startRenderLoop(true);
  const scriptInterface = builder.create(); 

  scriptInterface.add_ready(onWWTReady);
}

window.addEventListener("load", onLoad)
