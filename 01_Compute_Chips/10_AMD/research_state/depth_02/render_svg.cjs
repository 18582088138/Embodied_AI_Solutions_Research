// Offline artifact rendering only. Browser network requests are blocked.
const fs=require('fs'),path=require('path');
const {chromium}=require('C:/Users/kundaxu/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const crypto=require('crypto');
const project=path.resolve(__dirname,'../..'),arc=path.join(project,'reference_metrial');
const registry=JSON.parse(fs.readFileSync(path.join(arc,'_registry/materials.json'),'utf8'));
const items=[['02A_hip_threads','AMD_HIP_Model','thread_hierarchy.svg'],['02A_hip_memory','AMD_HIP_Model','memory_hierarchy.svg'],['02A_hip_graph','AMD_HIP_Graphs','hip_graph.svg'],['02A_hip_graph_timing','AMD_HIP_Graphs','hip_graph_speedup.svg']];
const sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'}),figures=[];
 try{
  for(const [slug,sid,tail] of items){
   const a=registry[sid].assets.find(x=>x.url.endsWith('/'+tail));if(!a)throw Error(tail);
   const original=path.join(arc,a.local_file||a.file),svg=fs.readFileSync(original,'utf8');
   const page=await browser.newPage({viewport:{width:2400,height:2400},deviceScaleFactor:1});
   await page.route('**/*',r=>r.abort());
   await page.setContent('<html><head><meta charset="utf-8"><style>body{margin:0;background:white}svg{display:block}</style></head><body>'+svg.replace(/<\?xml[^>]*>/g,'')+'</body></html>');
   await page.evaluate(()=>document.fonts.ready);
   const box=await page.locator('svg').boundingBox();
   await page.setViewportSize({width:Math.ceil(box.width)+1,height:Math.ceil(box.height)+1});
   const out=path.join(arc,'derived/figures',slug+'.png');
   await page.locator('svg').screenshot({path:out});
   figures.push({slug,source_id:sid,source_url:a.url,original_file:original.replace(/\\/g,'/'),original_sha256:sha(original),file:out.replace(/\\/g,'/'),sha256:sha(out),operation:'Chromium原SVG完整截图，保留foreignObject标签；白底，无裁剪/内容修改；网络禁用，系统字体替代'});
   await page.close();
  }
 }finally{await browser.close()}
 fs.writeFileSync(path.join(__dirname,'figures_A.json'),JSON.stringify(figures,null,2));
 process.stdout.write(JSON.stringify(figures.map(x=>({slug:x.slug,file:x.file})),null,2));
})().catch(e=>{process.stderr.write(String(e));process.exit(1)});
