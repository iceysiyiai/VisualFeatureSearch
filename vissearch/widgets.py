import random

# common JS code for executing callbacks into Python
CALLBACK_JS = '''
<script>
    function isCallbackSupported() {
        return (typeof Jupyter !== 'undefined') || (typeof google !== 'undefined');
    }

    function executeCallback(function_name, data) {
        if (typeof Jupyter !== 'undefined') {
            let call_statement = function_name + '("' + data + '")';
            Jupyter.notebook.kernel.execute(call_statement);
        } else if (typeof google !== 'undefined') {
            google.colab.kernel.invokeFunction(function_name, [data], {});
        }
    }
</script>
'''

HIGHLIGHT_HTML = '''
<p>
<div class="container" style="width: {sz}px; height: {sz}px;">
    <div class="image" style="background-image: url('{url}'); width: {sz}px; height: {sz}px;"></div>
    <canvas 
        id="drawCanvas_{N}"
        class="overlay" 
        style="z-index: 10; width: {sz}px; height: {sz}px;"
    ></canvas>
</div>
<svg  width="30" height="200">
        <rect
          y = "0"
          id="barplot"
          width="30"
          height="200"
          style="fill: green; stroke-width: 2; stroke: rgb(0, 0, 0)"
        />
      </svg>
</p>

<br>
<button id="resetBtn_{N}">Reset</button>

<style>
    .container {{
        position: relative;
        display: inline-block;
    }}

    .image, .overlay {{
        position: absolute;
        left: 0px;
        top: 0px;
    }}

    .overlay {{
        opacity: 0.5;
        transition: opacity .1s ease-in-out;
    }}

    .overlay:hover {{
        opacity: 0.7;
    }}
</style>

<script>
(function() {{
    let resetBtn = document.getElementById('resetBtn_{N}');
    let drawCanvas = document.getElementById('drawCanvas_{N}');

    drawCanvas.width = {sz};
    drawCanvas.height = {sz};
    let ctx = drawCanvas.getContext('2d');

    let drawing = false;

    function mouseDown() {{
        drawing = true;
    }}

    async function mouseUp() {{
        drawing = false;
        if('{callName}' !== 'None') {{
            executeCallback('{callName}', drawCanvas.toDataURL());
            let num = 50;
            await fetch('out.txt')
                .then(response => response.text())
                .then(text => {{
                    num = parseFloat(text);
                }});
            console.log(num);
            document.getElementById('barplot').setAttribute("height", 200*num);
        }}
    }}
    
    function processData(allText) {{
        alert(allText);
        
        
        return allText;
    }}

    function handleMove(e) {{
        if(!drawing) return;
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(e.offsetX, e.offsetY, {hlghtRad}, 0, 2 * Math.PI);
        ctx.fill();
    }}

    function reset() {{
        ctx.clearRect(0, 0, {sz}, {sz});
        document.getElementById('barplot').setAttribute("height", 200);
        if('{callName}' !== 'None') {{
            executeCallback('{callName}', drawCanvas.toDataURL());
        }}
    }}
    
    drawCanvas.onmousedown = mouseDown;
    drawCanvas.onmouseup = mouseUp;
    drawCanvas.onmousemove = handleMove;

    resetBtn.onclick = reset;
}})();


</script>
'''

########################################################################

MULTI_HIGHLIGHT_HTML = '''
<div style="height: {sz}px; margin-bottom: 5px;">
    <div class="container" style="width: {sz}px; height: {sz}px; float: left">
        <div class="image" id="currImgDiv_{N}" style="width: {sz}px; height: {sz}px;"></div>

        <canvas 
            id="drawCanvas_{N}"
            class="overlay" 
            style="z-index: 10; width: {sz}px; height: {sz}px;"
        ></canvas>
    </div>

    <div class="photos" id="photosDiv_{N}" style="height: {sz}px; float: left;">
    </div>
</div>

<button id="resetBtn_{N}">Reset</button>

<style>
    .container {{
        position: relative;
        display: inline-block;
    }}

    .image, .overlay {{
        position: absolute;
        left: 0px;
        top: 0px;
    }}

    .overlay {{
        opacity: 0.5;
        transition: opacity .1s ease-in-out;
    }}

    .overlay:hover {{
        opacity: 0.7;
    }}

    .photos {{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        /* justify-content: space-between; */
        flex-wrap: wrap;
        gap: 6px;

        margin-left: 10px;
        border-left: 3px solid black;
        padding-left: 10px;
    }}

    .photoBtn {{
        width: 40px;
        height: 40px;
        margin-top: 0px !important;
        margin-right: 2px;
        flex-basis: 40px;

        transition: opacity .05s ease-in-out;
    }}

    .photoBtn:hover {{
        opacity: 0.7;
    }}
</style>

<script>
(function() {{
    let photosDiv = document.getElementById('photosDiv_{N}');
    let currImgDiv = document.getElementById('currImgDiv_{N}');
    let resetBtn = document.getElementById('resetBtn_{N}');
    let drawCanvas = document.getElementById('drawCanvas_{N}');

    drawCanvas.width = {sz};
    drawCanvas.height = {sz};
    let ctx = drawCanvas.getContext('2d');

    let drawing = false;
    let urls = {urls};
    let selected = 0;

    function mouseDown() {{
        console.log('hello');
        drawing = true;
    }}

    function mouseUp() {{
        drawing = false;
        if('{callName}' !== 'None') {{
            executeCallback('{callName}', [drawCanvas.toDataURL(), selected]);
        }}
    }}

    function handleMove(e) {{
        if(!drawing) return;
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(e.offsetX, e.offsetY, {hlghtRad}, 0, 2 * Math.PI);
        ctx.fill();
    }}

    function reset() {{
        console.log('reset');
        ctx.clearRect(0, 0, {sz}, {sz});
        if('{callName}' !== 'None') {{
            executeCallback('{callName}', [drawCanvas.toDataURL(), selected]);
        }}
    }}

    function photoChange(e) {{
        let idVal = e.target.id;
        let index = idVal.split('_')[1];
        if(selected != index) {{
            selected = index;
            currUrl = urls[selected];
            currImgDiv.style.backgroundImage = "url('" + currUrl + "')";
            reset();
        }}
    }}

    for(let i = 0; i < urls.length; i++) {{
        let elem = document.createElement('img');
        elem.classList.add("photoBtn");
        elem.id = "photoBtn{N}_" + i;
        elem.src = urls[i];
        elem.onclick = photoChange;
        photosDiv.append(elem);
    }}

    currImgDiv.style.backgroundImage = "url('" + urls[0] + "')";

    drawCanvas.onmousedown = mouseDown;
    drawCanvas.onmouseup = mouseUp;
    drawCanvas.onmousemove = handleMove;

    resetBtn.onclick = reset;
    console.log(resetBtn);
}})();
</script>
'''

class HighlightWidget:
    ''' A Jupyter notebook widget for interactively selecting a specific region within an image.'''
    def __init__(self, img_url, callback_name=None, size=224, highlight_radius=20):
        self._img_url = img_url
        self._callback_name = callback_name
        self._size = size
        self._highlight_radius = highlight_radius

        # use a random number to ensure we never repeat identical HTML IDs
        self._id_suffix = random.randint(0, 1000000000)

    def _repr_html_(self):
        return CALLBACK_JS + HIGHLIGHT_HTML.format(
            N = self._id_suffix,
            sz = self._size, 
            url = self._img_url, 
            hlghtRad = self._highlight_radius,
            callName = self._callback_name
        )

class MultiHighlightWidget:
    def __init__(self, all_urls, callback_name=None, size=224, highlight_radius=20):
        self._all_urls = all_urls
        self._callback_name = callback_name
        self._size = size
        self._highlight_radius = highlight_radius

        # use a random number to ensure we never repeat identical HTML IDs
        self._id_suffix = random.randint(0, 1000000000)

    def _repr_html_(self):
        return CALLBACK_JS + MULTI_HIGHLIGHT_HTML.format(
            N = self._id_suffix,
            sz = self._size,
            urls = self._all_urls,
            hlghtRad = self._highlight_radius,
            callName = self._callback_name
        )