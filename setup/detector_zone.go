package setup

import (
	"encoding/json"
	"fmt"
)

// DetectorZones ...
type DetectorZones struct {
	Zones []ZoneID `json:"zones"`
}

// MarshalJSON json.Marshaller implementation.
func (d DetectorZones) MarshalJSON() ([]byte, error) {
	type Alias DetectorZones
	return json.Marshal(struct {
		Type string `json:"type"`
		Alias
	}{
		Type:  detectorGeometryType.zone,
		Alias: Alias(d),
	})
}

// Validate ...
func (d DetectorZones) Validate() error {
	if len(d.Zones) == 0 {
		return fmt.Errorf("list of zones can't be empty")
	}
	return nil
}
