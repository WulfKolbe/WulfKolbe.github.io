## Main use case
Please note that the original intention was to enlarge the function of the Claude.ai skill "reading a pdf" and therefore all components are developed to run inside Claude.ai sandbox. The sandbox has already installed a lot of tools.
 
## Code generation by Claude.ai / CLI 
Unfortunately the Claude CLI and Claude.ai deviated from my plans and took of into Python to generate the complete project. Only the drillui_bridge is a bun based Typescript web page. I have never touched the code myself. {{Gemini_Generated_Image_n0eqp8n0eqp8n0eq.png}}
My task was only to shout and scream at the constantly cheating Claude CLI's and do provide some test data.

## Some very old gimmicks - BlobTracker (from the last millennium)
 I have a background in industrial high-speed image processing and therefore some allergic reaction if the CLI gnerated code that loads again and again some heavy hitters like OPNECV for some totally trivial tasks.
Therefore I have given the CLI some very old C-code as an example how to tack blobs (org. code belongs to ISAVISION GmbH Kiel project SQS published in ([ext[JOT1997-03|./files/jot-bericht.pdf]]).

## Original idea to run inside Tiddlywiki 
This project has started as a Typescript project that could be transpiled to run in simple HTML page like HTML Tiddler of Tiddlywiki. My older Typescript code was able to access MathPix using the lines.json format and access GTPT4 image preview for pix to Latex task and Perplexity for BibTeX retrieval and Deepl.com for translation inside Tiddlywiki.  

## Tiddlywiki on Markdown and Google OKF 
Tiddlywiki can work directly with Markdown files and some *.meta files containing all the TW fields.
My typical use case is to generate symbolic links to all SKILL files in the TW tiddlers folder. Restart of the server will create all the meta files. Editing Skill file can be a real fun using TW.

### Please note how to see the skills
The constant cheat mode of Claude CLI can be "useful" with prompt like this: 
Please create a JSON Array of Tiddlers from your skill files. To generate a Tiddler title use the full path name. Use all the output from the ls -lha as fields of the json Tiddler structure and put the text in the text field of the Tiddler. 
For tests try to import it into a single HTML file Tiddlywiki.
