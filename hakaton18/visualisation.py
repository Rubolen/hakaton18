import lasio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class LasProcessing:

    def __init__(self, file_name: str):
        self.df_borders = pd.read_excel('Отбивки пласта АС11-2.xlsx')
        self.file_name = file_name
        self.las_read = lasio.read(f"las/{self.file_name}")

    def get_graphics_continuous(self, x_axis_name: str, y_axis_name: str) -> None:
        """
        Строит графики по данным из las файла
        :param x_axis_name: Столбец из las файла для оси x (можно выбрать 'NEU' или 'GGKP')
        :param y_axis_name: Столбец из las файла для оси x (можно выбрать 'DEPT ', 'SSTVD' или 'Z')
        :return: None
        """

        x_axis = self.las_read[x_axis_name]
        y_axis = self.las_read[y_axis_name]

        top_border_index = np.where(self.las_read['Z'].round(1) == round(self.get_borders()[0], 1))
        bottom_border_index = np.where(self.las_read['Z'].round(1) == round(self.get_borders()[1], 1))

        plt.figure(figsize=(10, 20), dpi=80)
        color = 'black'
        plt.xlabel(f"{x_axis_name}", fontsize=20)
        plt.ylabel(f"{y_axis_name}", fontsize=20)
        plt.title(f"{self.file_name[:-4]}", fontsize=20)
        plt.plot(x_axis[top_border_index[0][0]: bottom_border_index[0][0]],
                 y_axis[top_border_index[0][0]: bottom_border_index[0][0]], color=color,
                 label=str('NEU'))
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.show()

    def get_borders(self) -> list:
        """
        ВОзвращает границы пласта из таблицы 'Отбивки пласта АС11-2.xlsx'
        """
        border_filter_condition = self.file_name[:self.file_name.find('_')]
        try:
            top_border = self.df_borders[(self.df_borders['Well identifier'] == int(border_filter_condition)) & (
                    self.df_borders['Surface'] == 'АС11-1')]
            bottom_border = self.df_borders[((self.df_borders['Well identifier']) == int(border_filter_condition)) & (
                    self.df_borders['Surface'] == 'АС11-2')]
            return [top_border['Z'].iloc[0], bottom_border['Z'].iloc[0]]
        except:
            top_border = self.df_borders[(self.df_borders['Well identifier'] == border_filter_condition) & (
                    self.df_borders['Surface'] == 'АС11-1')]
            bottom_border = self.df_borders[((self.df_borders['Well identifier']) == border_filter_condition) & (
                    self.df_borders['Surface'] == 'АС11-2')]
            return [top_border['Z'].iloc[0], bottom_border['Z'].iloc[0]]

    def las_to_csv(self):
        self.las_read.to_csv(self.file_name, units_loc='[]')
        # df_excel = pd.read_excel(f'{self.file_name[:-4]}.xlsx', sheet_name='Curves')
        # df_excel.drop(
        #     df_excel[(df_excel['Z'] < self.get_borders()[0]) & (df_excel['Z'] > self.get_borders()[1])].index)


a = LasProcessing("12_continuous.las")
a.get_graphics_continuous('NEU', 'DEPT')
a.las_to_csv()
