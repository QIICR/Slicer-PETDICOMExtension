#include "dcmHelpersCommon.h"
#include "dcmtk/config/osconfig.h"
#include "dcmtk/dcmdata/dctk.h"
#include "dcmtk/dcmsr/dsriodcc.h"
#include "dcmtk/dcmsr/dsrdoc.h"

#define WARN_IF_ERROR(X,M) X

// List of tags copied from David Clunie's Pixelmed toolkit

const DcmTagKey dcmHelpersCommon::patientModuleTags[] = {
  DCM_PatientName,
  DCM_PatientID,
  //Macro IssuerOfPatientIDMacro
  DCM_IssuerOfPatientID,
  DCM_IssuerOfPatientIDQualifiersSequence,
  //EndMacro IssuerOfPatientIDMacro
  DCM_PatientBirthDate,
  DCM_PatientSex,
  DCM_QualityControlSubject,
  DCM_PatientBirthTime,
  DCM_ReferencedPatientSequence,
  DCM_OtherPatientIDsSequence,
  DCM_OtherPatientNames,
  DCM_EthnicGroups,
  DCM_PatientComments,
  DCM_PatientSpeciesDescription,
  DCM_PatientSpeciesCodeSequence,
  DCM_PatientBreedDescription,
  DCM_PatientBreedCodeSequence,
  DCM_BreedRegistrationSequence,
  DCM_ResponsiblePerson,
  DCM_ResponsiblePersonRole,
  DCM_ResponsibleOrganization,
  DCM_PatientIdentityRemoved,
  DCM_DeidentificationMethod,
  DCM_DeidentificationMethodCodeSequence
};

const DcmTagKey dcmHelpersCommon::clinicalTrialSubjectModuleTags[] = {
  DCM_ClinicalTrialSubjectID,
  DCM_ClinicalTrialSponsorName,
  DCM_ClinicalTrialProtocolID,
  DCM_ClinicalTrialProtocolName,
  DCM_ClinicalTrialSiteID,
  DCM_ClinicalTrialSiteName,
  DCM_ClinicalTrialSubjectID,
  DCM_ClinicalTrialSubjectReadingID
};

const DcmTagKey dcmHelpersCommon::generalStudyModuleTags[] = {
  DCM_StudyInstanceUID,
  DCM_StudyDate,
  DCM_StudyTime,
  DCM_ReferringPhysicianName,
  DCM_ReferringPhysicianIdentificationSequence,
  DCM_StudyID,
  DCM_AccessionNumber,
  DCM_IssuerOfAccessionNumberSequence,
  DCM_StudyDescription,
  DCM_PhysiciansOfRecord,
  DCM_PhysiciansOfRecordIdentificationSequence,
  DCM_NameOfPhysiciansReadingStudy,
  DCM_PhysiciansReadingStudyIdentificationSequence,
  DCM_RequestingServiceCodeSequence,
  DCM_ReferencedStudySequence,
  DCM_ProcedureCodeSequence,
  DCM_ReasonForPerformedProcedureCodeSequence
};

const DcmTagKey dcmHelpersCommon::patientStudyModuleTags[] = {
  DCM_AdmittingDiagnosesDescription,
  DCM_AdmittingDiagnosesCodeSequence,
  DCM_PatientAge,
  DCM_PatientSize,
  DCM_PatientWeight,
  DCM_PatientSizeCodeSequence,
  DCM_Occupation,
  DCM_AdditionalPatientHistory,
  DCM_AdmissionID,
  DCM_IssuerOfAdmissionIDSequence,
  DCM_ServiceEpisodeID,
  DCM_IssuerOfServiceEpisodeIDSequence,
  DCM_ServiceEpisodeDescription,
  DCM_PatientSexNeutered
};

const DcmTagKey dcmHelpersCommon::generalSeriesModuleTags[] = {
  DCM_Modality,
  DCM_SeriesInstanceUID,
  DCM_SeriesNumber,
  DCM_Laterality,
  DCM_SeriesDate,
  DCM_SeriesTime,
  DCM_PerformingPhysicianName,
  DCM_PerformingPhysicianIdentificationSequence,
  DCM_ProtocolName,
  DCM_SeriesDescription,
  DCM_SeriesDescriptionCodeSequence,
  DCM_OperatorsName,
  DCM_OperatorIdentificationSequence,
  DCM_ReferencedPerformedProcedureStepSequence,
  DCM_RelatedSeriesSequence,
  DCM_BodyPartExamined,
  DCM_PatientPosition,
  //DCM_SmallestPixelValueInSeries,
  //DCM_LargestPixelValueInSeries,
  DCM_RequestAttributesSequence,
  //Macro PerformedProcedureStepSummaryMacro
  DCM_PerformedProcedureStepID,
  DCM_PerformedProcedureStepStartDate,
  DCM_PerformedProcedureStepStartTime,
  DCM_PerformedProcedureStepDescription,
  DCM_PerformedProtocolCodeSequence,
  DCM_CommentsOnThePerformedProcedureStep,
  //EndMacro PerformedProcedureStepSummaryMacro
  DCM_AnatomicalOrientationType
};

const DcmTagKey dcmHelpersCommon::generalEquipmentModuleTags[] = {
  DCM_Manufacturer,
  DCM_InstitutionName,
  DCM_InstitutionAddress,
  DCM_StationName,
  DCM_InstitutionalDepartmentName,
  DCM_ManufacturerModelName,
  DCM_DeviceSerialNumber,
  DCM_SoftwareVersions,
  DCM_GantryID,
  DCM_SpatialResolution,
  DCM_DateOfLastCalibration,
  DCM_TimeOfLastCalibration,
  DCM_PixelPaddingValue
};

const DcmTagKey dcmHelpersCommon::frameOfReferenceModuleTags[] = {
  DCM_FrameOfReferenceUID,
  DCM_PositionReferenceIndicator
};

const DcmTagKey dcmHelpersCommon::sopCommonModuleTags[] = {
  DCM_SOPClassUID,
  DCM_SOPInstanceUID,
  //DCM_SpecificCharacterSet,
  DCM_InstanceCreationDate,
  DCM_InstanceCreationTime,
  DCM_InstanceCreatorUID,
  DCM_RelatedGeneralSOPClassUID,
  DCM_OriginalSpecializedSOPClassUID,
  DCM_CodingSchemeIdentificationSequence,
  DCM_TimezoneOffsetFromUTC,
  DCM_ContributingEquipmentSequence,
  DCM_InstanceNumber,
  DCM_SOPInstanceStatus,
  DCM_SOPAuthorizationDateTime,
  DCM_SOPAuthorizationComment,
  DCM_AuthorizationEquipmentCertificationNumber,
  //Macro DigitalSignaturesMacro
  //DCM_MACParametersSequence,
  //DCM_DigitalSignaturesSequence,
  //EndMacro DigitalSignaturesMacro
  //DCM_EncryptedAttributesSequence,
  DCM_OriginalAttributesSequence,
  DCM_HL7StructuredDocumentReferenceSequence
};

const DcmTagKey dcmHelpersCommon::generalImageModuleTags[] = {
  DCM_ContentDate,
  DCM_ContentTime
};

const DcmTagKey dcmHelpersCommon::srDocumentGeneralModuleTags[] = {
  DCM_ReferencedRequestSequence,    // cw. RequestAttributesSequence in GeneralSeries
  DCM_PerformedProcedureCodeSequence  // cw. ProcedureCodeSequence in GeneralStudy
};


void dcmHelpersCommon::copyElement(const DcmTagKey tag, DcmDataset *src, DcmDataset *dest){
  DcmElement *e;
  OFCondition cond;

  cond = src->findAndGetElement(tag, e, OFFalse, OFTrue);
  if(cond.good()){
    cond = dest->insert(e, true);
    dest->findAndGetElement(tag,e);
    char *str;
    e->getString(str);
    if(str)
      std::cout << "Inserted: " << str << std::endl;
    }
};


void dcmHelpersCommon::copyPatientModule(DcmDataset *src, DcmDataset *dest){
  for(unsigned int i=0;i<sizeof(patientModuleTags)/sizeof(DcmTagKey);i++)
    dcmHelpersCommon::copyElement(patientModuleTags[i], src, dest);
}

void dcmHelpersCommon::copyPatientStudyModule(DcmDataset *src, DcmDataset *dest){
  for(unsigned int i=0;i<sizeof(patientStudyModuleTags)/sizeof(DcmTagKey);i++)
    dcmHelpersCommon::copyElement(patientStudyModuleTags[i], src, dest);
}

void dcmHelpersCommon::copyGeneralStudyModule(DcmDataset *src, DcmDataset *dest){
  for(unsigned int i=0;i<sizeof(generalStudyModuleTags)/sizeof(DcmTagKey);i++)
    dcmHelpersCommon::copyElement(generalStudyModuleTags[i], src, dest);
}

void dcmHelpersCommon::copyClinicalTrialSubjectModule(DcmDataset *src, DcmDataset *dest){
  for(unsigned int i=0;i<sizeof(clinicalTrialSubjectModuleTags)/sizeof(DcmTagKey);i++)
    dcmHelpersCommon::copyElement(clinicalTrialSubjectModuleTags[i], src, dest);
}

/*
void dcmHelpersCommon::findAndGetCodedValueFromSequenceItem(DcmItem *seq,
                                                            DSRCodedEntryValue &codedEntry){
  char *elementStr;
  std::string codeMeaning, codeValue, codingSchemeDesignator;
  DcmElement *element;

  if(seq->findAndGetElement(DCM_CodeValue, element).good()){
    element->getString(elementStr);
    codeValue = std::string(elementStr);
  }

  if(seq->findAndGetElement(DCM_CodeMeaning, element).good()){
    element->getString(elementStr);
    codeMeaning = std::string(elementStr);
  }

  if(seq->findAndGetElement(DCM_CodingSchemeDesignator, element).good()){
    element->getString(elementStr);
    codingSchemeDesignator = std::string(elementStr);
  }

  codedEntry.setCode(codeValue.c_str(), codingSchemeDesignator.c_str(),
                     codeMeaning.c_str());
}
*/

void dcmHelpersCommon::addLanguageOfContent(DSRDocument *doc){
  doc->getTree().addContentItem(DSRTypes::RT_hasConceptMod, DSRTypes::VT_Code, DSRTypes::AM_belowCurrent);
  doc->getTree().getCurrentContentItem().setConceptName(
                DSRCodedEntryValue("121049", "DCM", "Language of Content Item and Descendants"));
  doc->getTree().getCurrentContentItem().setCodeValue(
                DSRCodedEntryValue("eng","RFC3066","English"));

  doc->getTree().addContentItem(DSRTypes::RT_hasConceptMod, DSRTypes::VT_Code, DSRTypes::AM_belowCurrent);
  doc->getTree().getCurrentContentItem().setConceptName(
                DSRCodedEntryValue("121046", "DCM", "Country of Language"));
  doc->getTree().getCurrentContentItem().setCodeValue(
                DSRCodedEntryValue("US","ISO3166_1","United States"));
  doc->getTree().goUp();
}

void dcmHelpersCommon::addObservationContext(DSRDocument *doc){
  dcmHelpersCommon::addObserverContext(doc);
  dcmHelpersCommon::addProcedureContext(doc);
  dcmHelpersCommon::addSubjectContext(doc);
}

// TODO: parameterize the actual values initialized
void dcmHelpersCommon::addObserverContext(DSRDocument *doc, const char* deviceObserverUID,
                                          const char* deviceObserverName, const char* deviceObserverManufacturer,
                                          const char* deviceObserverModelName, const char* deviceObserverSerialNumber){
    // TODO: TID 1001 Observation context
    doc->getTree().addContentItem(DSRTypes::RT_hasObsContext, DSRTypes::VT_Code, DSRTypes::AM_afterCurrent);
    doc->getTree().getCurrentContentItem().setConceptName(
                DSRCodedEntryValue("121005","DCM","Observer Type"));
    doc->getTree().getCurrentContentItem().setCodeValue(
                DSRCodedEntryValue("121007","DCM","Device"));

    // TODO: need to decide what UIDs we will use
    doc->getTree().addContentItem(DSRTypes::RT_hasObsContext, DSRTypes::VT_UIDRef, DSRTypes::AM_afterCurrent);
    doc->getTree().getCurrentContentItem().setConceptName(
                DSRCodedEntryValue("121012","DCM","Device Observer UID"));
    doc->getTree().getCurrentContentItem().setStringValue(deviceObserverUID);

    doc->getTree().addContentItem(DSRTypes::RT_hasObsContext, DSRTypes::VT_Text, DSRTypes::AM_afterCurrent);
    doc->getTree().getCurrentContentItem().setConceptName(
                DSRCodedEntryValue("121013","DCM","Device Observer Name"));
    doc->getTree().getCurrentContentItem().setStringValue(deviceObserverName);

    doc->getTree().addContentItem(DSRTypes::RT_hasObsContext, DSRTypes::VT_Text, DSRTypes::AM_afterCurrent);
    doc->getTree().getCurrentContentItem().setConceptName(
                DSRCodedEntryValue("121014","DCM","Device Observer Manufacturer"));
    doc->getTree().getCurrentContentItem().setStringValue(deviceObserverManufacturer);

    doc->getTree().addContentItem(DSRTypes::RT_hasObsContext, DSRTypes::VT_Text, DSRTypes::AM_afterCurrent);
    doc->getTree().getCurrentContentItem().setConceptName(
                DSRCodedEntryValue("121015","DCM","Device Observer Model Name"));
    doc->getTree().getCurrentContentItem().setStringValue(deviceObserverModelName);

    doc->getTree().addContentItem(DSRTypes::RT_hasObsContext, DSRTypes::VT_Text, DSRTypes::AM_afterCurrent);
    doc->getTree().getCurrentContentItem().setConceptName(
                DSRCodedEntryValue("121016","DCM","Device Observer Serial Number"));
    doc->getTree().getCurrentContentItem().setStringValue(deviceObserverSerialNumber);
}

void dcmHelpersCommon::addProcedureContext(DSRDocument *doc){
  // TODO
  (void) doc; // avoid warning: unused parameter 
}

void dcmHelpersCommon::addSubjectContext(DSRDocument *doc){
  // TODO
  (void) doc; // avoid warning: unused parameter 
}

/*
 * Add Image Library entry (TID 4020) for the specified SR document
 * and DcmDataset correspnding to an image to the document.
 */
void dcmHelpersCommon::addImageLibraryEntry(DSRDocument *doc, DcmDataset *imgDataset){
    DcmElement *element;
    DcmItem *sequenceItem;

    std::string sopClassUID, sopInstanceUID;
    char* elementStr;
    //float* elementFloat;
    OFString elementOFString;

    imgDataset->findAndGetElement(DCM_SOPClassUID, element);
    element->getString(elementStr);
    sopClassUID = std::string(elementStr);

    imgDataset->findAndGetElement(DCM_SOPInstanceUID, element);
    element->getString(elementStr);
    sopInstanceUID = std::string(elementStr);

    doc->getTree().addContentItem(DSRTypes::RT_contains,DSRTypes::VT_Image,
                                  DSRTypes::AM_belowCurrent);

    DSRImageReferenceValue imageReference =
            DSRImageReferenceValue(sopClassUID.c_str(), sopInstanceUID.c_str());
    doc->getTree().getCurrentContentItem().setImageReference(imageReference);

    DSRCodedEntryValue codedValue;

    DSRTypes::E_AddMode addMode = DSRTypes::AM_belowCurrent;

    // Image Laterality
    if(imgDataset->findAndGetSequenceItem(DCM_ImageLaterality,sequenceItem).good()){
       codedValue.readSequence(*imgDataset, DCM_ImageLaterality,"2");
       //findAndGetCodedValueFromSequenceItem(sequenceItem, codedValue);
       doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                     DSRTypes::VT_Code,
                                     DSRTypes::AM_belowCurrent);
       addMode = DSRTypes::AM_afterCurrent;
       doc->getTree().getCurrentContentItem().setConceptName(
                     DSRCodedEntryValue("111027","DCM","Image Laterality"));
       doc->getTree().getCurrentContentItem().setCodeValue(codedValue);
    }

    // Image View
    if(imgDataset->findAndGetSequenceItem(DCM_ViewCodeSequence,sequenceItem).good()){
      //findAndGetCodedValueFromSequenceItem(sequenceItem,codedValue);
      codedValue.readSequence(*imgDataset, DCM_ViewCodeSequence, "2");
      doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                    DSRTypes::VT_Code,
                                    addMode);
      addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;
      doc->getTree().getCurrentContentItem().setConceptName(
                  DSRCodedEntryValue("111031","DCM","Image View"));
      doc->getTree().getCurrentContentItem().setCodeValue(codedValue);

      //if(imgDataset->findAndGetSequenceItem(DCM_ViewModifierCodeSequence,sequenceItem).good()){
      if(codedValue.readSequence(*imgDataset, DCM_ViewModifierCodeSequence, "2").good()){
        //findAndGetCodedValueFromSequenceItem(sequenceItem,codedValue);
        doc->getTree().addContentItem(DSRTypes::RT_hasConceptMod,
                                      DSRTypes::VT_Code,
                                      DSRTypes::AM_belowCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                        DSRCodedEntryValue("111032","DCM","Image View Modifier"));
        doc->getTree().getCurrentContentItem().setCodeValue(codedValue);
        doc->getTree().goUp();
      }
    }

    // Patient Orientation - Row and Column separately
    if(imgDataset->findAndGetElement(DCM_PatientOrientation, element).good()){
        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                                    DSRTypes::VT_Text,
                                                    addMode);

        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("111044","DCM","Patient Orientation Row"));
        doc->getTree().getCurrentContentItem().setStringValue(elementOFString.c_str());

        element->getOFString(elementOFString, 1);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Text,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("111043","DCM","Patient Orientation Column"));
        doc->getTree().getCurrentContentItem().setStringValue(elementOFString.c_str());
    }

    // Study date
    if(imgDataset->findAndGetElement(DCM_StudyDate, element).good()){
        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                                    DSRTypes::VT_Date,
                                                    addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("111060","DCM","Study Date"));
        doc->getTree().getCurrentContentItem().setStringValue(elementOFString.c_str());
    }

    // Study time
    if(imgDataset->findAndGetElement(DCM_StudyTime, element).good()){

        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Time,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("111061","DCM","Study Time"));
        doc->getTree().getCurrentContentItem().setStringValue(elementOFString.c_str());
    }

    // Content date
    if(imgDataset->findAndGetElement(DCM_ContentDate, element).good()){

        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Date,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("111018","DCM","Content Date"));
        doc->getTree().getCurrentContentItem().setStringValue(elementOFString.c_str());
    }

    // Content time
    if(imgDataset->findAndGetElement(DCM_ContentTime, element).good()){
        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Time,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("111019","DCM","Content Time"));
        doc->getTree().getCurrentContentItem().setStringValue(elementOFString.c_str());
    }

    // Pixel Spacing - horizontal and vertical separately
    if(imgDataset->findAndGetElement(DCM_PixelSpacing, element).good()){
        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("111026","DCM","Horizontal Pixel Spacing"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("mm","UCUM","millimeter")));

        element->getOFString(elementOFString, 1);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("111066","DCM","Vertical Pixel Spacing"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("mm","UCUM","millimeter")));
    }

    // Positioner Primary Angle
    if(imgDataset->findAndGetElement(DCM_PositionerPrimaryAngle, element).good()){

        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("112011","DCM","Positioner Primary Angle"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("deg","UCUM","degrees of plane angle")));

    }

    // Positioner Secondary Angle
    if(imgDataset->findAndGetElement(DCM_PositionerSecondaryAngle, element).good()){

        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("112012","DCM","Positioner Secondary Angle"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("deg","UCUM","degrees of plane angle")));
    }

    // TODO
    // Spacing between slices: May be computed from the Image Position (Patient) (0020,0032)
    // projected onto the normal to the Image Orientation (Patient) (0020,0037) if present;
    // may or may not be the same as the Spacing Between Slices (0018,0088) if present.

    // Slice thickness/
    if(imgDataset->findAndGetElement(DCM_SliceThickness, element).good()){

        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("112225","DCM","Slice Thickness"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("mm","UCUM","millimeter")));
    }

    // Frame of reference
    if(imgDataset->findAndGetElement(DCM_FrameOfReferenceUID, element).good()){

        element->getOFString(elementOFString,0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_UIDRef,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("112227","DCM","Frame of Reference UID"));
        doc->getTree().getCurrentContentItem().setStringValue(elementOFString);
    }

    // Image Position Patient
    if(imgDataset->findAndGetElement(DCM_ImagePositionPatient, element).good()){
        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110901","DCM","Image Position (Patient) X"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("mm","UCUM","millimeter")));

        element->getOFString(elementOFString, 1);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110902","DCM","Image Position (Patient) Y"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("mm","UCUM","millimeter")));

        element->getOFString(elementOFString, 2);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110903","DCM","Image Position (Patient) Z"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("mm","UCUM","millimeter")));
    }

    // Image Orientation Patient
    if(imgDataset->findAndGetElement(DCM_ImageOrientationPatient, element).good()){
        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110904","DCM","Image Orientation (Patient) Row X"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("{-1:1}","UCUM","{-1:1}")));

        element->getOFString(elementOFString, 1);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110905","DCM","Image Orientation (Patient) Row Y"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("{-1:1}","UCUM","{-1:1}")));

        element->getOFString(elementOFString, 2);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110906","DCM","Image Orientation (Patient) Row Z"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("{-1:1}","UCUM","{-1:1}")));

        element->getOFString(elementOFString, 3);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110907","DCM","Image Orientation (Patient) Column X"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("{-1:1}","UCUM","{-1:1}")));

        element->getOFString(elementOFString, 4);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110908","DCM","Image Orientation (Patient) Column Y"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("{-1:1}","UCUM","{-1:1}")));

        element->getOFString(elementOFString, 5);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110909","DCM","Image Orientation (Patient) Column Z"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("{-1:1}","UCUM","{-1:1}")));

    }

    // Image Orientation Patient
    if(imgDataset->findAndGetElement(DCM_Rows, element).good()){
        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      addMode);
        addMode = addMode == DSRTypes::AM_belowCurrent ? DSRTypes::AM_afterCurrent : addMode;

        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110910","DCM","Pixel Data Rows"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("{pixels}","UCUM","pixels")));

        imgDataset->findAndGetElement(DCM_Columns, element);
        element->getOFString(elementOFString, 0);
        doc->getTree().addContentItem(DSRTypes::RT_hasAcqContext,
                                      DSRTypes::VT_Num,
                                      DSRTypes::AM_afterCurrent);
        doc->getTree().getCurrentContentItem().setConceptName(
                    DSRCodedEntryValue("110911","DCM","Pixel Data Columns"));
        doc->getTree().getCurrentContentItem().setNumericValue(
                    DSRNumericMeasurementValue(elementOFString.c_str(),
                                               DSRCodedEntryValue("{pixels}","UCUM","pixels")));
    }


    doc->getTree().goUp(); // up to image level
    doc->getTree().goUp(); // up to image library container level
}
