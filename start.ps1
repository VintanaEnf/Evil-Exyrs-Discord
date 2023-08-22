
function main(){
    Clear-Host
    Write-Output "--------------------------------------------------------"
    Write-Output "note: keys.py is needed for the bot to function properly"
    Write-Output ""
    Write-Output "you can manually configure everything by editing const.py"
    Write-Output "or let the script generate and configure for you."
    Write-Output "--------------------------------------------------------"
    Write-Output ""
    Write-Output "press '0' to start the bot."
    Write-Output "press '1' for the script to generate keys.py"
    Write-Output "press '2' to locate keys.py in your machine"
    Write-Output ""
    $in = Read-Host "Input: "
    if($in -eq 0){
        run_bot
    }
    
}

function run_bot(){
    Write-Output "Starting bot..."
    Clear-Host
    Set-Location .\src
python3 .\main.py
}

main