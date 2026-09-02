---
title: asp.net core 發佈 cesium terrain 懸崖
date: 2026-02-10 05:56:00
tags:
- cesium
- asp.net core
- gis
---
&nbsp;
<!-- more -->

<iframe 
width="1036" 
height="772" 
src="https://www.youtube.com/embed/0ZpSE70K1zc?list=RD0ZpSE70K1zc" 
title="懸崖" 
frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
referrerpolicy="strict-origin-when-cross-origin" 
allowfullscreen></iframe>


快過年了, 好久沒有去懸崖非常想念, 決定復刻下, 整理作品順便把以前的咚咚弄得更有 fu 點 XD
舊版可以看[這裡](https://www.blog.lasai.com.tw/posts/asp-net-core-%E7%99%BC%E4%BD%88-cesium-terrain/)

圖資可以到這裡[下載](https://www.tgos.tw/TGOS/NgdaMap)

建 terrain 的工具 [cesium-terrain-builder-docker](https://github.com/tum-gis/cesium-terrain-builder-docker)

host
```
docker pull ghcr.io/tum-gis/ctb-quantized-mesh:latest
# 可以看看下載的 image
# docker images

mkdir cesium
cd cesium

# 可以到這個網站找 DTM
# https://www.tgos.tw/TGOS/NgdaMap
wget "https://www.tgos.tw:443/MDE/VirtualDir_TC/Product/528530be-0710-431e-954e-2f2f5e98b0c5/不分幅_全台20MDEM(2025).zip"

# 應該是會缺少 unzip 這個解壓工具
sudo apt install unzip

# 重新命名
mv '不分幅_全台20MDEM(2025).zip' tw2025.zip

# 解壓縮
unzip tw2025.zip

# 應該會出現 tif 檔
ls
# DEM_tawiwan_V2025.tfw  DEM_tawiwan_V2025.tif  Metadata.xml  manifest.csv  tw2025.zip

# 進入 ctb
docker run -it --name ctb -v "${PWD}:/data" tumgis/ctb-quantized-mesh

# 離開的話
# exit

# 如果再次進入可以這樣下
# docker ps -a
# CONTAINER ID   IMAGE                       COMMAND   CREATED          STATUS                      PORTS     NAMES
# 4a2d3a5eca0c   tumgis/ctb-quantized-mesh   "bash"    41 minutes ago   Exited (0) 30 minutes ago             ctb

# docker start ctb
# docker exec -it ctb bash
```


container
```
# 把投影轉換 4326
gdalwarp -s_srs EPSG:3826 -t_srs EPSG:4326 -r bilinear -of GTiff DEM_tawiwan_V2025.tif DEM_tawiwan_V2025_4326.tif

# 準備資料夾讓他放
mkdir terrain

# 生成 layer.json
ctb-tile -f Mesh -C -N -l -o terrain DEM_tawiwan_V2025_4326.tif

# 生 terrain
ctb-tile -f Mesh -C -N -o terrain DEM_tawiwan_V2025_4326.tif

# 退出容器
exit
```

回到 host 用 windows 檔案總管開啟並且複製
```
explorer.exe .
```

## asp.net core 8

建一個 .net 8 的 asp.net core 專案, 下載 [Cesium](https://cesium.com/downloads/)
將 `Build` 裡面的 `CesiumUnminified` 丟到你專案內的 `wwwroot` 資料夾內
並且把開頭算好的 `terrain` 資料夾也丟到 `wwwroot` 裡面
並且把 `CesiumUnminified` 跟 `terrain` 都設定 `Exclude from project` 防止太多檔案導致 `visual studio` 速度變慢

csproj
```
<Project Sdk="Microsoft.NET.Sdk.Web">

	<PropertyGroup>
		<TargetFramework>net8.0</TargetFramework>
		<Nullable>enable</Nullable>
		<ImplicitUsings>enable</ImplicitUsings>
	</PropertyGroup>

	<ItemGroup>
		<PackageReference Include="Swashbuckle.AspNetCore" Version="6.6.2" />

		<Content Remove="wwwroot\terrain\**;wwwroot\CesiumUnminified\**" />
		<None Remove="wwwroot\terrain\**;wwwroot\CesiumUnminified\**" />
		<Compile Remove="wwwroot\terrain\**;wwwroot\CesiumUnminified\**" />
		<EmbeddedResource Remove="wwwroot\terrain\**;wwwroot\CesiumUnminified\**" />
	</ItemGroup>

	<ItemGroup>
	  <Folder Include="wwwroot\" />
	</ItemGroup>

	<PropertyGroup>
		<DefaultItemExcludes>$(DefaultItemExcludes);wwwroot\terrain\**;wwwroot\CesiumUnminified\**</DefaultItemExcludes>
	</PropertyGroup>

</Project>

```

後端則需要設定 CORS 還有 static file 並且讓 terrain 檔案被認得

`Program.cs`
```
using Microsoft.AspNetCore.StaticFiles;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseCors(builder =>
{
    builder.AllowAnyOrigin();
    builder.AllowAnyMethod();
    builder.AllowAnyHeader();
});

var provider = new FileExtensionContentTypeProvider();
provider.Mappings.Add(".terrain", "application/vnd.quantized-mesh");

app.UseStaticFiles(new StaticFileOptions
{
    ContentTypeProvider = provider,
    OnPrepareResponse = ctx =>
    {
        string extension = System.IO.Path.GetExtension(ctx.File.Name);
        if (extension == ".terrain")
        {
            ctx.Context.Response.Headers.Add("Content-Encoding", "gzip");
        }
    },
});

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();

```

接著調整 `launchSettings.json` 裡面的 `port` `https 5001` `http 5000`

最後則是前端, 因為新版已經有變動所以請用以下的程式碼即可, 懸崖真是美極了

在 `wwwroot` 底下建立 `index.html`
```
<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cesium - 精確座標定位</title>
    <link rel="stylesheet" href="/CesiumUnminified/Widgets/widgets.css">
    <style>
        html, body, #cesiumContainer { width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden; background-color: #000; }

        /* 資訊面板樣式 */
        #info-panel {
            position: absolute;
            bottom: 30px;
            left: 10px;
            background: rgba(0, 0, 0, 0.85);
            color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            z-index: 1000;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            min-width: 240px;
        }
        .section-title { color: #ffcc00; font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid #444; padding-bottom: 4px; }
        .item { margin: 4px 0; display: flex; justify-content: space-between; }
        .label { color: #aaa; }
        .value { color: #00ffcc; font-weight: bold; text-align: right; margin-left: 10px; }
        hr { border: 0; border-top: 1px solid #444; margin: 10px 0; }

        /* 複製按鈕 */
        #copy-btn {
            width: 100%;
            background: #007bff;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
            margin-top: 5px;
            pointer-events: auto;
        }
        #copy-btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div id="cesiumContainer"></div>
    
    <div id="info-panel">
        <div class="section-title">📍 目前座標 (Camera)</div>
        <div class="item"><span class="label">緯度:</span><span id="cam-lat" class="value">-</span></div>
        <div class="item"><span class="label">經度:</span><span id="cam-lon" class="value">-</span></div>
        <div class="item"><span class="label">高度:</span><span id="cam-hgt" class="value">-</span> m</div>
        
        <hr>
        
        <div class="section-title">🎥 鏡頭角度</div>
        <div class="item"><span class="label">方位 (H):</span><span id="cam-heading" class="value">-</span>°</div>
        <div class="item"><span class="label">俯仰 (P):</span><span id="cam-pitch" class="value">-</span>°</div>
        <div class="item"><span class="label">翻滾 (R):</span><span id="cam-roll" class="value">-</span>°</div>
        
        <button id="copy-btn">複製目前視角資訊</button>
    </div>

    <script>window.CESIUM_BASE_URL = '/CesiumUnminified/';</script>
    <script src="/CesiumUnminified/Cesium.js"></script>

    <script>
        async function startCesium() {
            try {
                // 1. 初始化 Viewer
                const viewer = new Cesium.Viewer('cesiumContainer', {
                    baseLayer: new Cesium.ImageryLayer(
                        new Cesium.UrlTemplateImageryProvider({
                            url: 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                            minimumLevel: 1,
                            maximumLevel: 20
                        })
                    ),
                    animation: false,
                    timeline: false,
                    geocoder: false,
                    baseLayerPicker: false,
                    scene3DOnly: true
                });

                // 2. 【核心設定】根據你提供的參數進行開場定位
                // 緯度: 21.929914, 經度: 120.845648, 高度: 122.55m
                viewer.camera.setView({
                    destination: Cesium.Cartesian3.fromDegrees(120.845648, 21.929914, 122.55),
                    orientation: {
                        heading: Cesium.Math.toRadians(10.20),
                        pitch: Cesium.Math.toRadians(-13.58),
                        roll: Cesium.Math.toRadians(360.00) // 等同於 0.0
                    }
                });

                // 3. 載入地形
                try {
                    const terrainProvider = await Cesium.CesiumTerrainProvider.fromUrl('/terrain', {
                        requestVertexNormals: true
                    });
                    viewer.terrainProvider = terrainProvider;
                    // 關鍵：開啟深度檢測，讓低空視角下地形與相機的互動更自然
                    viewer.scene.globe.depthTestAgainstTerrain = true;
                } catch (e) { console.warn("地形載入失敗"); }

                // 4. 更新 UI 面板
                const ui = {
                    lon: document.getElementById('cam-lon'),
                    lat: document.getElementById('cam-lat'),
                    hgt: document.getElementById('cam-hgt'),
                    head: document.getElementById('cam-heading'),
                    pit: document.getElementById('cam-pitch'),
                    rol: document.getElementById('cam-roll')
                };

                function updateStats() {
                    const camera = viewer.camera;
                    const cartographic = Cesium.Cartographic.fromCartesian(camera.position);
                    
                    ui.lat.textContent = Cesium.Math.toDegrees(cartographic.latitude).toFixed(6);
                    ui.lon.textContent = Cesium.Math.toDegrees(cartographic.longitude).toFixed(6);
                    ui.hgt.textContent = cartographic.height.toFixed(2);
                    
                    ui.head.textContent = Cesium.Math.toDegrees(camera.heading).toFixed(2);
                    ui.pit.textContent = Cesium.Math.toDegrees(camera.pitch).toFixed(2);
                    ui.rol.textContent = Cesium.Math.toDegrees(camera.roll).toFixed(2);
                }

                viewer.camera.changed.addEventListener(updateStats);
                updateStats();

                // 5. 複製功能
                document.getElementById('copy-btn').onclick = function() {
                    const textToCopy = `座標: ${ui.lat.textContent}, ${ui.lon.textContent}\n` +
                                     `高度: ${ui.hgt.textContent}m\n` +
                                     `角度: H:${ui.head.textContent}°, P:${ui.pit.textContent}°, R:${ui.rol.textContent}°`;
                    
                    navigator.clipboard.writeText(textToCopy).then(() => {
                        const originalText = this.innerText;
                        this.innerText = "✅ 已複製到剪貼簿";
                        setTimeout(() => this.innerText = originalText, 1500);
                    });
                };

            } catch (error) { console.error(error); }
        }

        startCesium();
    </script>
</body>
</html>

```
