UnityWebRequest

exemeple : 

using UnityEngine.Networking;
using UnityEngine;

public class APIManager : MonoBehaviour
{
    private string baseURL = "http://localhost:5000";

    public void GetPlayers()
    {
        StartCoroutine(GetRequest($"{baseURL}/players/"));
    }

    IEnumerator GetRequest(string url)
    {
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log(request.downloadHandler.text);
        }
        else
        {
            Debug.LogError(request.error);
        }
    }
}