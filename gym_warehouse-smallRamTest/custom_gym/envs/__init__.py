from gym.envs.registration import register

register(id='Warehouse-v0',
    entry_point='envs.warehouse:WarehouseEnv'
)
