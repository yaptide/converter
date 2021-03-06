package material

import (
	"testing"

	"github.com/yaptide/converter/common/color"
	test "github.com/yaptide/converter/test"
)

var testCases = test.MarshallingCases{
	{
		&Material{ID(1), color.New(0xFF, 0x00, 0x00, 0xFF), Predefined{PredefinedID: "methanol"}},
		`{
			"id": 1,
			"color": {
				"r": 255,
				"g": 0,
				"b": 0,
				"a": 255
			},
			"materialInfo": {
				"type": "predefined",
				"predefinedId": "methanol"
			}
		}`,
	},
	{
		&Material{ID(1), color.New(0xFF, 0x00, 0x00, 0xFF), Predefined{
			PredefinedID:              "methanol",
			StateOfMatter:             Liquid,
			Density:                   0.001,
			LoadExternalStoppingPower: false,
		}},
		`{
			"id": 1,
			"color": {
				"r": 255,
				"g": 0,
				"b": 0,
				"a": 255
			},
			"materialInfo": {
				"type": "predefined",
				"predefinedId": "methanol",
				"density": 0.001,
				"stateOfMatter": "liquid"
			}
		}`,
	},
	{
		&Material{ID(1), color.New(0xFF, 0xFF, 0xFF, 0xFF), Compound{
			Name:          "ala",
			Density:       1.2345,
			StateOfMatter: Gas,
			Elements: []Element{
				Element{Isotope: "As-75", RelativeStoichiometricFraction: 1},
				Element{Isotope: "H-1 - Hydrogen", RelativeStoichiometricFraction: 8},
			},
		}},
		`{
			"id": 1,
			"color": {
				"r": 255,
				"g": 255,
				"b": 255,
				"a": 255
			},
			"materialInfo": {
				"type": "compound",
				"name": "ala",
				"density": 1.2345,
				"stateOfMatter": "gas",
				"elements": [
					{
						"isotope": "As-75",
						"relativeStoichiometricFraction": 1
					},
					{
						"isotope": "H-1 - Hydrogen",
						"relativeStoichiometricFraction": 8
					}
				]
			}
		}`,
	},
	{
		&Material{ID(1), color.New(0xAA, 0xBB, 0xCC, 0xFF), Compound{
			Name:          "kot",
			Density:       99.9,
			StateOfMatter: Liquid,
			Elements: []Element{
				Element{Isotope: "Gd-*", RelativeStoichiometricFraction: 2, AtomicMass: 100.23},
				Element{Isotope: "U-235", RelativeStoichiometricFraction: 123, IValue: 555.34},
			},
			ExternalStoppingPowerFromPredefined: "Water",
		}},
		`{
			"id": 1,
			"color": {
				"r": 170,
				"g": 187,
				"b": 204,
				"a": 255
			},
			"materialInfo": {
				"type": "compound",
				"name": "kot",
				"density": 99.9,
				"stateOfMatter": "liquid",
				"elements": [
					{
						"isotope": "Gd-*",
						"relativeStoichiometricFraction": 2,
						"atomicMass": 100.23
					},
					{
						"isotope": "U-235",
						"relativeStoichiometricFraction": 123,
						"iValue": 555.34
					}
				],
				"externalStoppingPowerFromPredefined": "Water"
			}
		}`,
	},
}

func TestSetupMarshal(t *testing.T) {
	test.Marshal(t, testCases)
}

func TestSetupUnmarshal(t *testing.T) {
	test.Unmarshal(t, testCases)
}

func TestSetupUnmarshalMarshalled(t *testing.T) {
	test.UnmarshalMarshalled(t, testCases)
}

func TestSetupMarshalUnmarshalled(t *testing.T) {
	test.MarshalUnmarshalled(t, testCases)
}
