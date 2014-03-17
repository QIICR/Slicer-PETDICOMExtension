#ifndef __dcmHelpersCommon_h
#define __dcmHelpersCommon_h

#include <vector>

class DcmItem;
class DcmTagKey;
class DcmDataset;
class DSRDocument;
class DSRCodedEntryValue;

class dcmHelpersCommon {
  protected:
    static const DcmTagKey patientModuleTags[];
    static const DcmTagKey clinicalTrialSubjectModuleTags[];
    static const DcmTagKey generalStudyModuleTags[];
    static const DcmTagKey patientStudyModuleTags[];
    static const DcmTagKey generalSeriesModuleTags[];
    static const DcmTagKey generalEquipmentModuleTags[];
    static const DcmTagKey frameOfReferenceModuleTags[];
    static const DcmTagKey sopCommonModuleTags[];
    static const DcmTagKey generalImageModuleTags[];
    static const DcmTagKey srDocumentGeneralModuleTags[];


  public:

    static void copyElement(const DcmTagKey, DcmDataset *src, DcmDataset *dest);
    static void copyPatientModule(DcmDataset *src, DcmDataset *dest);
    static void copyClinicalTrialSubjectModule(DcmDataset *src, DcmDataset *dest);
    static void copyGeneralStudyModule(DcmDataset *src, DcmDataset *dest);
    static void copyPatientStudyModule(DcmDataset *src, DcmDataset *dest);
    static void copyGeneralSeriesModule(DcmDataset *src, DcmDataset *dest);
    static void copyGeneralEquipmentModule(DcmDataset *src, DcmDataset *dest);
    static void copyFrameOfReferenceModule(DcmDataset *src, DcmDataset *dest);
    static void copySOPCommonModule(DcmDataset *src, DcmDataset *dest);
    static void copyGeneralImageModule(DcmDataset *src, DcmDataset *dest);
    static void copySRDocumentGeneralModule(DcmDataset *src, DcmDataset *dest);


    //static void copyItems(DcmDataset *src, DcmDataset *dest);

    // functions to initialize specific templates; return to the same level in the input
    // -- TID 4020 "CAD Image Library Entry Template"
    // this function adds an
    static void addImageLibraryEntry(DSRDocument*, DcmDataset*);
    // -- TID 1204 "Language of Content Item and Descendants"
    static void addLanguageOfContent(DSRDocument*);
    // -- TID 1001 "Observation context"
    static void addObservationContext(DSRDocument*);
    // -- TID 1002 "Observer context"
    static void addObserverContext(DSRDocument*,const char* deviceObserverUID = "",
                                   const char* deviceObserverName ="", const char* deviceObserverManufacturer = "",
                                   const char* deviceObserverModelName ="", const char* deviceObserverSerialNumber = "");
    // -- TID 1005 "Procedure context"
    static void addProcedureContext(DSRDocument*);
    // -- TID 1006 "Subject context"
    static void addSubjectContext(DSRDocument*);

    //static void addCurrentRequestedProcedureEvidenceSequence(std::vector<DcmDataset*>& ,
    //                                                            DcmDataset*);
};

#endif
