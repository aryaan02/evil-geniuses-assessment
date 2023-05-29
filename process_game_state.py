import pandas as pd
import matplotlib.path as mpath


class ProcessGameState:
    def __init__(self, file_path):
        self.data = self.__ingest_data(file_path)
        # self.weapon_classes = self.get_weapon_classes()

    def __ingest_data(self, file_path):

        # Read in the data
        data = pd.read_parquet(file_path, engine='pyarrow')

        # Convert the clock time to a datetime object
        data['clock_time'] = data['clock_time'].replace('00:60', '01:00')
        data['clock_time'] = pd.to_datetime(
            data['clock_time'], format='%M:%S').dt.strftime('%M:%S')

        return data

    def __calculate_boundary(self, xy_bounds, z_bounds):

        # List of x and y coordinates
        x_coords = [point[0] for point in xy_bounds]
        y_coords = [point[1] for point in xy_bounds]

        # Get the min and max of the x, y, and z coordinates
        x_min = min(x_coords)
        x_max = max(x_coords)
        y_min = min(y_coords)
        y_max = max(y_coords)
        z_min = min(z_bounds)
        z_max = max(z_bounds)

        return {
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max,
            'z_min': z_min,
            'z_max': z_max
        }

    def __in_bounds(self, point, boundary):
        return point[0] >= boundary['x_min'] and point[0] <= boundary['x_max'] \
            and point[1] >= boundary['y_min'] and point[1] <= boundary['y_max'] \
            and point[2] >= boundary['z_min'] and point[2] <= boundary['z_max']

    def check_boundaries(self, xy_bounds, z_bounds, data_subset):

        # Get the boundary
        boundary = self.__calculate_boundary(xy_bounds, z_bounds)

        # Get the list of round numbers and sort them
        rounds = list(data_subset['round_num'].unique())
        rounds.sort()
        num_rounds = len(rounds)

        # Create a list to store the number of times the player is in bounds for each round
        num_in_bounds = [0] * num_rounds

        # Iterate through each round
        for round in rounds:
            in_count = 0
            curr_round = data_subset[data_subset['round_num'] == round]

            # Iterate through each row in the current round
            for _, row in curr_round.iterrows():
                point = (row['x'], row['y'], row['z'])

                # Check if the player is in bounds
                if self.__in_bounds(point, boundary):
                    in_count += 1

            # Store the number of times players are in bounds for the current round
            num_in_bounds[round % num_rounds] = in_count

        return num_in_bounds

    def check_boundaries_with_matplotlib(self, xy_bounds, z_bounds, data):

        # Get the list of round numbers and sort them
        rounds = list(data['round_num'].unique())
        rounds.sort()
        num_rounds = len(rounds)

        # Create a list to store the number of times the player is in bounds for each round
        num_in_bounds = [0] * num_rounds

        # Path object
        path = mpath.Path(xy_bounds)

        # Iterate through each round
        for round in rounds:
            in_count = 0
            curr_round = data[data['round_num'] == round]

            # Iterate through each row in the current round
            for _, row in curr_round.iterrows():
                point = (row['x'], row['y'])

                # Check if the player is in bounds
                if path.contains_point(point) and row['z'] >= z_bounds[0] and row['z'] <= z_bounds[1]:
                    in_count += 1

            # Store the number of times the player is in bounds for the current round
            num_in_bounds[round % num_rounds] = in_count

        return num_in_bounds

    # def get_weapon_classes(self):
    #     weapon_classes = set()
    #     for _, row in self.data.iterrows():
    #         if row['inventory'] is not None:
    #             for weapon in row['inventory']:
    #                 weapon_classes.add(weapon['weapon_class'])
    #         if len(weapon_classes) == 4:
    #             break
    #     return weapon_classes


game_state = ProcessGameState('data/game_state_frame_data.parquet')
