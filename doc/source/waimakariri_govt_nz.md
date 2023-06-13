# Waimakariri Council

Support for schedules provided by [Waimakariri Council](https://www.waimakariri.govt.nz/).

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: waimakariri_govt_nz
      args:
        house_number: 1
        street_name: Bell st
        town: Rangiora
        postcode: 7400
```

### Configuration Variables

**house_number**  
*(string) (required)*  
The house number of the address.

**street_name**  
*(string) (required)*  
The name of the street.

**town**  
*(string) (required)*  
The name of the town.

**postcode**  
*(string) (required)*  
The postal code of the address.

## Example

```yaml
waste_collection_schedule:
  sources:
    - name: waimakariri_govt_nz
      args:
        house_number: 1
        street_name: Bell st
        town: Rangiora
        postcode: 7400
```

## How to get the source arguments

The source arguments correspond to the address details required by the Waimakariri Council website:

1. Go to the calendar and search for your address: https://rethinkrubbish.waimakariri.govt.nz/s/#calendar
2. Copy the displayed address at the top (Note that it uses 'Bell St' not 'Bell street')