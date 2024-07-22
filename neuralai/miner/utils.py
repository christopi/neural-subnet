import bittensor as bt
import urllib.parse
import aiohttp
import time

def set_status(self, status: str="idle"):
    self.miner_status = status
    
def check_validator(self, uid: int, interval: int = 300):
    cur_time = time.time()
    bt.logging.debug(f"#######################111#####################")
    bt.logging.debug(f"{uid}")
    # bt.logging.debug(f"{self.validators}")
    if uid not in self.validators:
        bt.logging.debug(f"#######################222#####################")
        self.validators[uid] = {
            "start": cur_time,
            "requests": 1,
        }
        bt.logging.debug(f"{self.validators}")
        bt.logging.debug(f"#######################222#####################")
        
    elif cur_time - self.validators[uid]["start"] > interval:
        bt.logging.debug(f"#######################333#####################")
        
        self.validators[uid] = {
            "start": cur_time,
            "requests": 1,
        }
        bt.logging.debug(f"{self.validators}")
        bt.logging.debug(f"#######################333#####################")
        
    else:
        bt.logging.debug(f"#######################444#####################")
        self.validators[uid]["requests"] += 1
        bt.logging.debug(f"{self.validators}")
        
        bt.logging.debug(f"#######################444#####################")
        
        return True
    return False

async def generate(self, synapse: bt.Synapse) -> bt.Synapse:
    url = urllib.parse.urljoin(self.config.generation.endpoint, "/generate_from_text/")
    timeout = synapse.timeout
    # bt.logging.debug(f"timeout type: {type(timeout)}")
    prompt = synapse.prompt_text
    synapse_type = type(synapse).__name__
    
    if synapse_type is "NATextSynapse":
        result = await _generate_from_text(gen_url=url, timeout=timeout, prompt=prompt)
        bt.logging.debug(f"generation result: {type(result)}")
    
    synapse.out_obj = result
    
    return synapse

async def _generate_from_text(gen_url: str, timeout: int, prompt: str):
    async with aiohttp.ClientSession() as session:
        try:
            bt.logging.debug(f"=================================================")
            client_timeout = aiohttp.ClientTimeout(total=float(timeout))
            
            async with session.post(gen_url, timeout=client_timeout, data={"prompt": prompt}) as response:
                if response.status == 200:
                    result = await response.text()
                    bt.logging.info(f"Generated successfully: Size = {len(result)}")
                    return result
                else:
                    bt.logging.error(f"Generation failed. Please try again.: {response.status}")
        except aiohttp.ClientConnectorError:
            bt.logging.error(f"Failed to connect to the endpoint. Try to access again: {gen_url}.")
        except TimeoutError:
            bt.logging.error(f"The request to the endpoint timed out: {gen_url}")
        except aiohttp.ClientError as e:
            bt.logging.error(f"An unexpected client error occurred: {e} ({gen_url})")
        except Exception as e:
            bt.logging.error(f"An unexpected error occurred: {e} ({gen_url})")