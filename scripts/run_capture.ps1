param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("photos", "video", "lidar")]
    [string] $Tier,

    [Parameter(Mandatory = $true)]
    [string] $InputPath,

    [Parameter(Mandatory = $true)]
    [string] $OutputPath
)

python -m cozmo_scan.cli --tier $Tier --input $InputPath --output $OutputPath
