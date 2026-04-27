from winchunker import ingestDoc, submit_chunks
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn
import argparse
print("PROGRAM STARTING...")
print("_"*20)
def ensurerange(x):
    """Ensures threshold arg range is within 0<->1"""
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid threshold float {x}")
    
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError(f"invalid threshold outside of range {x}")
    return x
parser = argparse.ArgumentParser(description="Starts the Semantic Window Chunker server")
parser.add_argument("--threshold", type=ensurerange, help="Threshold for semantic cutoff - float between 0 and 1. Default value 0.6.")
parser.add_argument("--min_size", type=int, help="Integer count of minimum charachter count in a chunk.")
parser.add_argument("--w_size", type=int, help="Integer size of window for semantic chunking. Default value 6.")
parser.add_argument("--url", type=str, help="Supabase url, obtained from .env file in directory if it exists.")
parser.add_argument("--key", type=str, help="Supabase key, obtained from .env file in directory if it exists. A Secret/Service key is prefferable for this as it is a backend service but other keys can be arraged with proper row level security on supabase.")
parser.add_argument("--model", type=str, help="Huggingface model. Default value MongoDB/mdbr-leaf-mt.")
args = parser.parse_args()
app = FastAPI();


print("WARMUP COMPLETE, SERVER UP...")
print("_"*20)


class CReq(BaseModel):
    text: str
    table: str
    docid: str
 
@app.post("/process-text", status_code=status.HTTP_200_OK)
async def process_text(request: CReq):
    try:
        parg = [request.text]
        keyword_args = {}
        if args.min_size != None:
            keyword_args["min_size"] = args.min_size
        if args.threshold != None:
            keyword_args["thresh"] = args.threshold
        if args.model != None:    
            keyword_args["modelname"] = args.model
        if args.w_size != None:
            keyword_args["window"] = args.w_size
        
        chunks = ingestDoc(*parg, **keyword_args)
        #chunks = ingestDoc(request.text, 50, 0.6)
        if args.url != None and args.key != None:
            submit_chunks(request.table, chunks, request.docid, url, key)
        else:
            submit_chunks(request.table, chunks, request.docid)
        return {"response": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, port=8000)