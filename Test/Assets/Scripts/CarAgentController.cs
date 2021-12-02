using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class CarAgents
{
    public List<Vector3> positions;
}
public class CarAgentController : MonoBehaviour
{
     [SerializeField] string url;
     [SerializeField] string testEP;
     [SerializeField] string configEP;
     [SerializeField] private string updateEP;
     [SerializeField] private string updateCarAgentsEP;
//     // [SerializeField] private string updateBoxAgentsEP;
     [SerializeField] int numAgents;
//     // [SerializeField] int numBoxes;
     [SerializeField] private GameObject carAgentPrefab;
     [SerializeField] private GameObject trafficLightAgentPrefab;
     [SerializeField] private float timeToUpdate;
     
     CarAgents Agents;
     GameObject[] carAgents;

     List<Vector3> oldPos;
     List<Vector3> newPos;
   
     float timer, dt;
     
     // Pause the simulation while we get the update from the server
     bool hold = false;
     bool configureed = false;

     // Start is called before the first frame update
     void Start()
     {
         oldPos = new List<Vector3>();
         newPos = new List<Vector3>();

         carAgents = new GameObject[numAgents];

         timer = timeToUpdate;
         
         for (int i = 0; i < numAgents; i++)
         {
             carAgents[i] = Instantiate(carAgentPrefab, Vector3.zero, Quaternion.Euler(new Vector3(-90, 0, -90)));
         }
         
         StartCoroutine(SendConfig()); 
     }

     // Update is called once per frame
     void Update()
     {
         float t = timer / timeToUpdate;

         dt = t * t * (3f - 2f * t);
         if(configureed)
         {
             if(timer >= timeToUpdate)
             {
                 timer = 0;
                 hold = true;
                 StartCoroutine(UpdateSimulation());
             }
         
             if (!hold)
             {
                 MoveCarAgents();
                 // Move time from the last frame
                 timer += Time.deltaTime;
             }
         }
         
     }

     IEnumerator TestAPI()
     {
         UnityWebRequest www = UnityWebRequest.Get(url + testEP);
         yield return www.SendWebRequest();

         if (www.result == UnityWebRequest.Result.Success)
         {
             Debug.Log(www.downloadHandler.text);
         }
         else
         {
             Debug.Log(www.error);
         }
     }
     
     IEnumerator SendConfig()
     {
         WWWForm form = new WWWForm();
         form.AddField("numAgents", numAgents.ToString());

         UnityWebRequest www = UnityWebRequest.Post(url + configEP, form);
         yield return www.SendWebRequest();

         if (www.result == UnityWebRequest.Result.Success)
         {
             StartCoroutine(GetCarData());
             Debug.Log(www.downloadHandler.text);
         }
         else
         {
             Debug.Log(www.error);
         }

         configureed = true;
     }
     
     IEnumerator UpdateSimulation()
     {
         UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
         yield return www.SendWebRequest();
  
         if (www.result != UnityWebRequest.Result.Success)
             Debug.Log(www.error);
         else
         {
             StartCoroutine(GetCarData());
         }
     }

     IEnumerator GetCarData()
     {
         UnityWebRequest www = UnityWebRequest.Get(url + updateCarAgentsEP);
         yield return www.SendWebRequest();
  
         if (www.result != UnityWebRequest.Result.Success)
             Debug.Log(www.error);
         else 
         { 
             Agents = JsonUtility.FromJson<CarAgents>(www.downloadHandler.text);
             oldPos = new List<Vector3>(newPos);

             newPos.Clear();
            
             foreach(Vector3 v in Agents.positions)
                 newPos.Add(v);

             if (oldPos.Count == 0)
             {
                 oldPos = new List<Vector3>(newPos);
             }
             
             hold = false;
         }
     }

     void MoveCarAgents()
     {
         for (int i = 0; i < numAgents; i++)
         {
             Vector3 interpolated = Vector3.Lerp(oldPos[i], newPos[i], dt);
             carAgents[i].transform.localPosition = interpolated;
                 
             Vector3 dir = oldPos[i] - newPos[i];
             carAgents[i].transform.rotation = Quaternion.LookRotation(dir);
         }
     }
}
