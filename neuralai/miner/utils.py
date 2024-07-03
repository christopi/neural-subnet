import bittensor as bt
import urllib.parse
import aiohttp


def set_status(self):
    miner_status = "idle"
    return miner_status

async def generate(self, synapse: bt.Synapse):
    url = urllib.parse.urljoin(self.config.generation.endpoint, "/generate/")
    timeout = synapse.timeout
    bt.logging.debug(f"timeout type: {type(timeout)}")
    prompt = synapse.prompt_text
    
    await _generate_from_text(gen_url=url, timeout=timeout, prompt=prompt)
    
    synapse.out_obj = "Time is Gold!!!"
    return synapse

async def _generate_from_text(gen_url: str, timeout: int, prompt: str):
    bt.logging.info(f"Generating from text. Generation prompt: {prompt}")
    bt.logging.debug(gen_url)
    
    async with aiohttp.ClientSession(timeout) as session:
        try:
            async with session.post(gen_url, data={"prompt": prompt}) as response:
                if response.status == 200:
                    bt.logging.info("Generated successfully")
                    result = await response.text()
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