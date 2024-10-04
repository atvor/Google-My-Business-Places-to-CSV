import pandas as pd


# def flatten_dict(d, parent_key='', sep='_'):
# TODO fix or create multiple headers
#     items = []
#     for k, v in d.items():
#         new_key = f'{parent_key}{sep}{k}' if parent_key else k
#         if isinstance(v, dict):
#             items.extend(flatten_dict(v, new_key, sep=sep).items())
#         else:
#             items.append((new_key, v))
#     return dict(items)


def write_dict_to_csv(data, filename):
    # Flatten the dictionary
    # flat_dict = flatten_dict(data)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Write to CSV
    df.to_csv(filename, index=False)
