from clusters.minidox import MinidoxCluster
import os
import json


class ItsydoxCluster(MinidoxCluster):

    @staticmethod
    def name():
        return "ITSYDOX"

    def get_config(self):
        with open(os.path.join("src", "clusters", "json", "ITSYDOX.json"), mode='r') as fid:
            data = json.load(fid)

        superdata = super().get_config()

        # overwrite any super variables with this class' needs
        for item in data:
            superdata[item] = data[item]

        for item in superdata:
            if not hasattr(self, str(item)):
                print(self.name() + ": NO MEMBER VARIABLE FOR " + str(item))
                continue
            setattr(self, str(item), superdata[item])

        return superdata

    def __init__(self, parent_locals):
        self.num_keys = 3
        super().__init__(parent_locals)
        # have to repeat this for all classes/namespaces
        for item in parent_locals:
            globals()[item] = parent_locals[item]

    def tl_place(self, shape):
        shape = rotate(shape, [10, -23, 25])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-35, -16, -2])
        return shape

    def tr_place(self, shape):
        shape = rotate(shape, [14, -15, 10])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-15, -10, 5])
        return shape

    def fl_place(self, shape):
        shape = rotate(shape, [0, -32, 40])
        shape = translate(shape, self.thumborigin())
        shape = translate(shape, [-25, -45, -15.5])
        return shape

    def thumb_1x_layout(self, shape, cap=False):
        debugprint('thumb_1x_layout()')
        return union([
            self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),
            self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation])),
        ])

    def thumb_fx_layout(self, shape):
        return union([
            self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),
            self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation])),
            # self.fl_place(rotate(shape, [0, 0, self.thumb_plate_bl_rotation])),
        ])
            
            
    def thumb_connectors(self, side="right"):
        print('thumb_connectors()')
        hulls = []

        # Top two
        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(self.thumb_post_tr()),
                    self.tl_place(self.thumb_post_br()),
                    self.tr_place(self.thumb_post_tl()),
                    self.tr_place(self.thumb_post_bl()),
                ]
            )
        )

        # bottom two on the right
        # hulls.append(
        #     triangle_hulls(
        #         [
        #             self.tl_place(self.thumb_post_tl()),
        #             self.tl_place(self.thumb_post_bl()),
        #             self.ml_place(self.thumb_post_tr()),
        #             self.ml_place(self.thumb_post_br()),
        #         ]
        #     )
        # )

        # top two to the main keyboard, starting on the left
        hulls.append(
            triangle_hulls(
                [
                    self.tl_place(self.thumb_post_tl()),
                    key_place(web_post_bl(), 0, lastrow),
                    self.tl_place(self.thumb_post_tr()),
                    key_place(web_post_br(), 0, lastrow),
                    self.tr_place(self.thumb_post_tl()),
                    key_place(web_post_bl(), 1, lastrow),
                    self.tr_place(self.thumb_post_tr()),
                    key_place(web_post_br(), 1, lastrow),
                    # key_place(web_post_tl(), 2, lastrow),
                    key_place(web_post_br(), 1, lastrow),
                    self.tr_place(self.thumb_post_tr()),
                    key_place(web_post_br(), 1, lastrow),
                    key_place(web_post_bl(), 2, lastrow),
                    key_place(web_post_br(), 2, lastrow),

                    key_place(web_post_bl(), 3, lastrow),

                    key_place(web_post_br(), 1, lastrow),
                    key_place(web_post_bl(), 3, lastrow),
                    key_place(web_post_br(), 2, lastrow),
                    key_place(web_post_bl(), 2, lastrow),
                    key_place(web_post_br(), 1, lastrow),

                    self.tr_place(self.thumb_post_tr()),
                    key_place(web_post_bl(), 3, lastrow),
                    # key_place(web_post_bl(), 3, lastrow),
                    self.tr_place(self.thumb_post_br()),
                    self.tr_place(self.thumb_post_tr()),
                    key_place(web_post_bl(), 3, lastrow),
                    # key_place(web_post_tr(), 2, lastrow),
                    # key_place(web_post_tl(), 3, lastrow),
                    # key_place(web_post_bl(), 3, lastrow),
                    # # key_place(web_post_tr(), 3, lastrow),
                    # key_place(web_post_br(), 3, lastrow),
                ]
            )
        )

        return union(hulls)

    def walls(self, side="right"):
        print('thumb_walls()')
        # thumb, walls
        shape = union([wall_brace(self.tr_place, 0, -1, self.thumb_post_br(), self.tr_place, 0, -1, self.thumb_post_bl())])
        shape = union([shape, wall_brace(self.tr_place, 0, -1, self.thumb_post_bl(), self.tl_place, 0, -1, self.thumb_post_br())])
        shape = union([shape, wall_brace(self.tl_place, 0, -1, self.thumb_post_br(), self.tl_place, 0, -1, self.thumb_post_bl())])
        shape = union([shape, wall_brace(self.tl_place, 0, -1, self.thumb_post_bl(), self.tl_place, -1, -1, self.thumb_post_br())])
        shape = union([shape, wall_brace(self.tl_place, -1, -1, self.thumb_post_br(), self.tl_place, 0, -1, self.thumb_post_bl())])
        shape = union([shape, wall_brace(self.tl_place, 0, -1, self.thumb_post_bl(), self.tl_place, -1, 0, self.thumb_post_bl())])
        # thumb, corners
        shape = union([shape, wall_brace(self.tl_place, -1, 0, self.thumb_post_bl(), self.tl_place, -1, 0, self.thumb_post_tl())])
        shape = union([shape, wall_brace(self.tl_place, -1, 0, self.thumb_post_tl(), self.tl_place, 0, 1, self.thumb_post_tl())])
        # thumb, tweeners
        shape = union([shape, wall_brace(self.tl_place, -1, 1, self.thumb_post_tl(), self.tl_place, 0, 1, self.thumb_post_tl())])
        shape = union([shape, wall_brace(self.tr_place, 0, -1, self.thumb_post_br(), (lambda sh: key_place(sh, 3, lastrow)), 0, -1, web_post_bl())])

        return shape

    def connection(self, side='right'):
        print('thumb_connection()')
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        shape = union([bottom_hull(
            [
                left_key_place(translate(web_post(), wall_locate2(-1, 0)), lastrow, -1, low_corner=True, side=side),
                left_key_place(translate(web_post(), wall_locate3(-1, 0)), lastrow, -1, low_corner=True, side=side),
                self.bl_place(translate(self.thumb_post_tr(), wall_locate2(-0.3, 1))),
                self.bl_place(translate(self.thumb_post_tr(), wall_locate3(-0.3, 1))),
            ]
        )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_key_place(translate(web_post(), wall_locate2(-1, 0)), lastrow, -1, low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate3(-1, 0)), lastrow, -1, low_corner=True, side=side),
                               self.tl_place(translate(self.thumb_post_tr(), wall_locate2(-0.3, 1))),
                               self.tl_place(translate(self.thumb_post_tr(), wall_locate3(-0.3, 1))),
                               self.tl_place(self.thumb_post_tl()),
                           ]
                       )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_key_place(web_post(), lastrow, -1, low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate1(-1, 0)), lastrow, -1, low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate2(-1, 0)), lastrow, -1, low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate3(-1, 0)), lastrow, -1, low_corner=True, side=side),
                               self.tl_place(self.thumb_post_tl()),
                           ]
                       )])

        shape = union([shape,
                       hull_from_shapes(
                           [
                               left_key_place(web_post(), lastrow, -1, low_corner=True, side=side),
                               left_key_place(translate(web_post(), wall_locate1(-1, 0)), lastrow, -1, low_corner=True, side=side),
                               key_place(web_post_bl(), 0, lastrow),
                               # key_place(translate(web_post_bl(), wall_locate1(-1, 0)), cornerrow, -1, low_corner=True),
                               self.tl_place(self.thumb_post_tl()),
                           ]
                       )])

        # shape = union([shape,
        #                hull_from_shapes(
        #                    [
        #                        self.tl_place(self.thumb_post_tr()),
        #                        self.tl_place(translate(self.thumb_post_tr(), wall_locate1(0, 1))),
        #                        self.tl_place(translate(self.thumb_post_tr(), wall_locate2(0, 1))),
        #                        self.tl_place(translate(self.thumb_post_tr(), wall_locate3(0, 1))),
        #                        self.tl_place(self.thumb_post_tl()),
        #                    ]
        #                )])

        return shape