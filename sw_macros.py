import clr

clr.AddReference(r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\api\redist\SolidWorks.Interop.sldworks.dll")
clr.AddReference(r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\api\redist\SolidWorks.Interop.cosworks.dll")
clr.AddReference(r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Runtime.InteropServices.dll")


import SolidWorks.Interop.sldworks as sw
import SolidWorks.Interop.cosworks as cw
import System.Runtime.InteropServices as Services


class Macro:

    def __init__(self, path_to_doc):
        # Подключение к приложению
        self._swApp = Services.Marshal.GetActiveObject("sldworks.application")
        self.swApp = sw.ISldWorks(self._swApp)

        # Документ
        self.swApp.OpenDoc(path_to_doc, 1)
        self._swDoc = self.swApp.ActiveDoc
        self.mDoc = sw.ModelDoc2(self._swDoc)
        self.pDoc = sw.PartDoc(self._swDoc)
        self.fs = sw.Feature(self.pDoc.FirstFeature())

    # получаем данные и расположение вставленных пузырей
    def get_bubbles_data(self):
        bubbles_definition = []
        bubbles_data = []
        i = 0
        while self.fs is not None:
            self.fs = sw.Feature(self.fs)
            if self.fs.GetTypeName().find("MoveCopyBody") != -1:
                bubbles_definition.append(self.fs.GetDefinition())
                print('count bubbles ' + str(i))
                i += 1
            self.fs = self.fs.GetNextFeature()

        for i in range(len(bubbles_definition)):
            data = sw.IMoveCopyBodyFeatureData(bubbles_definition[i])
            bubbles_data.append((data.TransformX, data.TransformY, data.TransformZ))

        return bubbles_data

    # вставляем пузыри
    def generic_bubbles(self, path_to_insert_object, count_bubbles=4):
        cw_program_id = "cosmosworks.cosmosworks"
        sw_simulation = cw.CwAddincallback(self.swApp.GetAddInObject(cw_program_id))
        sw_app = sw_simulation.CosmosWorks
        cw_doc = sw_app.ActiveDoc
        stud_man = cw_doc.StudyManager
        study = stud_man.GetStudy(0)
        ec_num = 0
        r_ncrd = [0.0, 0.0, 0.0]
        bbFFname = path_to_insert_object
        for i in range(count_bubbles):
            err_m = study.CreateMesh(0, 10.0, 0.5)
            fem = cw.CWMesh(study.Mesh)
            err_r = study.RunAnalysis()
            results = cw.CWResults(study.Results)
            sss, err_s = results.GetStrain(1, 1, None, 1)
            e_cnt = fem.ElementCount
            critical_extra = float(1.0)
            ad_ind, ad_step = 10, 13
            for j in range(1, e_cnt):
                sss_critical = float(sss[(j - 1) * ad_step + ad_ind])
                if sss_critical < critical_extra:
                    critical_extra = sss_critical
                    ec_num = j

            els = fem.GetElements()
            ad_ind, ad_step = 11, 16
            for k in range(3):
                r_ncrd[k] = float(els[(ec_num - 1) * ad_step + ad_ind + k])

            bubble = self.pDoc.InsertPart2(bbFFname, 513)
            p_bodies = self.pDoc.GetBodies2(0, True)
            bb_body = sw.Body2(p_bodies[p_bodies.Length - 1])
            self.mDoc.ClearSelection()
            bb_body.Select(True, -1)
            bubble = self.mDoc.FeatureManager.InsertMoveCopyBody2(r_ncrd[0], r_ncrd[1], r_ncrd[2],
                                                                  0, 0, 0, 0, 0, 0, 0, False, 1)
            p_bodies = self.pDoc.GetBodies2(0, True)
            m_body = sw.Body2(p_bodies[0])
            bb_body = sw.Body2(p_bodies[p_bodies.Length - 1])
            m_body.Select(True, -1)
            bb_body.Select(True, -1)
            bubble = self.mDoc.FeatureManager.InsertCombineFeature(15902, None, None)

    def add_bubble(self, path_to_insert_object, add_point):
        cw_program_id = "cosmosworks.cosmosworks"

        sw_simulation = cw.CwAddincallback(self.swApp.GetAddInObject(cw_program_id))
        sw_app = sw_simulation.CosmosWorks

        cw_doc = sw_app.ActiveDoc
        stud_man = cw_doc.StudyManager
        stud_man.GetStudy(0)

        bbFFname = path_to_insert_object
        self.pDoc.InsertPart2(bbFFname, 513)
        p_bodies = self.pDoc.GetBodies2(0, True)
        bb_body = sw.Body2(p_bodies[p_bodies.Length - 1])

        self.mDoc.ClearSelection()
        bb_body.Select(True, -1)
        self.mDoc.FeatureManager.InsertMoveCopyBody2(add_point[0], add_point[1], add_point[2],
                                                              0, 0, 0, 0, 0, 0, 0, False, 1)
        p_bodies = self.pDoc.GetBodies2(0, True)
        m_body = sw.Body2(p_bodies[0])
        bb_body = sw.Body2(p_bodies[p_bodies.Length - 1])
        m_body.Select(True, -1)
        bb_body.Select(True, -1)
        self.mDoc.FeatureManager.InsertCombineFeature(15902, None, None)