# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import numpy as np
from typing import List
import bittensor as bt


def reward(query: int, response: int, uids: List[int],) -> float:
    """
    Reward the miner response to the dummy request. This method returns a reward
    value for the miner, which is used to update the miner's score.

    Returns:
    - float: The reward value for the miner.
    """
    if response is None:
        bt.logging.info(
            f"In rewards, query val: {query}, response val: {response}, rewards val: 0"
        )
        return 0

    bt.logging.info(
        f"In rewards, query val: {query}, response val: {response}, rewards val: {1.0 if response/2 in uids else 0}"
    )

    # return 1.0 if response == query * 2 else 0
    return 1.0 if response/2 in uids else 0

def random_weight_map(uids):
    values = np.random.rand(len(uids))       # 生成 [0, 1) 之间的随机数
    values /= values.sum()                   # 归一化，使总和为 1
    return dict(zip(uids, values))           # 构建 map

def get_rewards(
    self,
    query: int,
    responses: List[float],
    uids: List[int],
) -> np.ndarray:
    """
    Returns an array of rewards for the given query and responses.

    Args:
    - query (int): The query sent to the miner.
    - responses (List[float]): A list of responses from the miner.

    Returns:
    - np.ndarray: An array of rewards for the given query and responses.
    """
    # Get all the reward results by iteratively calling your reward() function.

    # return np.array([reward(query, response, uids) for response in responses])

    result = random_weight_map(uids)
    valid_pairs = []
    for response in responses:
        target_uid = 0 if response is None else int(response / 2)
        valid_pairs.append(round(result[target_uid], 2)) if target_uid in uids else valid_pairs.append(0)

    valid_pairs[-1] = 1.0
    return valid_pairs

    # valid_pairs = [0.0] * len(responses)
    # if responses:
    #     valid_pairs[-1] = 1.0
    #
    # return np.array(valid_pairs)
